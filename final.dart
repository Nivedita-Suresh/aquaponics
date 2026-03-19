import 'dart:async';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const AquaponicsApp());
}

class AquaponicsApp extends StatelessWidget {
  const AquaponicsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Dashboard(),
    );
  }
}

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  final String url = 'http://192.168.4.1';
  static const double lowWaterLevelCm = 5.0;
  static const double highWaterLevelCm = 20.0;
  static const double lowTemperatureC = 22.0;
  static const double highTemperatureC = 30.0;
  static const double lowPh = 6.5;
  static const double highPh = 7.5;

  double distance = 0;
  double temperature = 0;
  double ph = 6.4;
  String lastFeedingTime = 'Unknown';
  bool pump1On = true;
  String waterLevelState = 'UNKNOWN';
  bool connected = false;
  String error = '';
  final List<_AlertLogEntry> alertLogs = <_AlertLogEntry>[];

  final List<double> distanceHistory = <double>[];
  final List<double> temperatureHistory = <double>[];

  Timer? timer;
  Timer? phReminderTimer;

  @override
  void initState() {
    super.initState();
    fetchData();
    timer = Timer.periodic(const Duration(seconds: 2), (_) => fetchData());
    phReminderTimer =
        Timer.periodic(const Duration(hours: 24), (_) => _showPhReminder());
  }

  @override
  void dispose() {
    timer?.cancel();
    phReminderTimer?.cancel();
    super.dispose();
  }

  Future<void> fetchData() async {
    try {
      final response =
          await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));

      if (response.statusCode != 200) {
        _setDisconnected('HTTP ${response.statusCode}');
        return;
      }

      final body = response.body;
      final distValue = _extractNumber(
        body,
        <String>['distance', 'water level', 'level', 'cm'],
      );
      final tempValue = _extractNumber(
        body,
        <String>['temperature', 'temp', 'c'],
      );
      final phValue = _extractNumber(
        body,
        <String>['ph', 'pH level'],
      );
      final feedingValue = _extractLastFeeding(body);

      if (distValue == null || tempValue == null || phValue == null) {
        _setDisconnected('Response format mismatch');
        return;
      }
      final waterEval = _evaluateWaterLevel(distValue);
      final tempEval = _evaluateTemperature(tempValue);
      final phEval = _evaluatePh(phValue);

      if (!mounted) return;
      setState(() {
        connected = true;
        error = '';
        distance = distValue;
        temperature = tempValue;
        ph = phValue;
        lastFeedingTime = feedingValue;
        waterLevelState = waterEval.code;

        if (distValue < lowWaterLevelCm) {
          pump1On = false;
        } else if (distValue > highWaterLevelCm) {
          pump1On = true;
        }

        distanceHistory.add(distValue);
        temperatureHistory.add(tempValue);

        if (distanceHistory.length > 20) {
          distanceHistory.removeAt(0);
        }
        if (temperatureHistory.length > 20) {
          temperatureHistory.removeAt(0);
        }

        _addLog(
          sensor: 'Water Level',
          value: '${distValue.toStringAsFixed(1)} cm',
          status: waterEval.logCode,
          message: waterEval.message,
          isAlert: waterEval.isAlert,
        );
        _addLog(
          sensor: 'Temperature',
          value: '${tempValue.toStringAsFixed(1)} C',
          status: tempEval.logCode,
          message: tempEval.message,
          isAlert: tempEval.isAlert,
        );
        _addLog(
          sensor: 'pH',
          value: ph.toStringAsFixed(1),
          status: phEval.logCode,
          message: phEval.message,
          isAlert: phEval.isAlert,
        );
      });
    } catch (e) {
      _setDisconnected(e.toString());
    }
  }

  void _setDisconnected(String message) {
    if (!mounted) return;
    setState(() {
      connected = false;
      error = message;
      waterLevelState = 'UNKNOWN';
      pump1On = false;
    });
  }

  double? _extractNumber(String body, List<String> labels) {
    final normalized = body.replaceAll('\r', '');
    for (final label in labels) {
      final pattern = RegExp(
        '${RegExp.escape(label)}\\s*[:=]?\\s*(-?\\d+(?:\\.\\d+)?)',
        caseSensitive: false,
      );
      final match = pattern.firstMatch(normalized);
      if (match != null) {
        return double.tryParse(match.group(1)!);
      }
    }

    // Fallback for simple JSON-like payloads.
    for (final label in labels) {
      final pattern = RegExp(
        '"${RegExp.escape(label)}"\\s*:\\s*(-?\\d+(?:\\.\\d+)?)',
        caseSensitive: false,
      );
      final match = pattern.firstMatch(normalized);
      if (match != null) {
        return double.tryParse(match.group(1)!);
      }
    }

    return null;
  }

  String _extractLastFeeding(String body) {
    final normalized = body.replaceAll('\r', '');
    final match = RegExp(
      r'Last\s*Feeding\s*[:=]\s*([^<\n]+)',
      caseSensitive: false,
    ).firstMatch(normalized);
    if (match != null) {
      return match.group(1)!.trim();
    }
    return 'Unknown';
  }

  _SensorEval _evaluateWaterLevel(double waterLevelCm) {
    if (waterLevelCm < lowWaterLevelCm) {
      return const _SensorEval(
        code: 'LOW',
        logCode: 'LOW_WATER_LEVEL',
        message: 'Water level critically low - refill aquarium immediately',
        isAlert: true,
      );
    }
    if (waterLevelCm <= highWaterLevelCm) {
      return const _SensorEval(
        code: 'NORMAL',
        logCode: 'WATER_LEVEL_OK',
        message: 'Water level normal',
        isAlert: false,
      );
    }
    return const _SensorEval(
      code: 'HIGH',
      logCode: 'HIGH_WATER_LEVEL',
      message: 'Water level too high - possible overflow risk',
      isAlert: true,
    );
  }

  _SensorEval _evaluateTemperature(double tempC) {
    if (tempC < lowTemperatureC) {
      return const _SensorEval(
        code: 'LOW',
        logCode: 'LOW_TEMPERATURE',
        message: 'Water temperature too low - heater recommended',
        isAlert: true,
      );
    }
    if (tempC <= highTemperatureC) {
      return const _SensorEval(
        code: 'NORMAL',
        logCode: 'TEMPERATURE_OK',
        message: 'Temperature normal',
        isAlert: false,
      );
    }
    return const _SensorEval(
      code: 'HIGH',
      logCode: 'HIGH_TEMPERATURE',
      message: 'Water temperature too high - cooling required',
      isAlert: true,
    );
  }

  _SensorEval _evaluatePh(double phValue) {
    if (phValue < lowPh) {
      return const _SensorEval(
        code: 'LOW',
        logCode: 'LOW_PH',
        message: 'Water too acidic - add buffering agent',
        isAlert: true,
      );
    }
    if (phValue <= highPh) {
      return const _SensorEval(
        code: 'NORMAL',
        logCode: 'PH_OK',
        message: 'pH level ideal',
        isAlert: false,
      );
    }
    return const _SensorEval(
      code: 'HIGH',
      logCode: 'HIGH_PH',
      message: 'Water too alkaline - adjust pH',
      isAlert: true,
    );
  }

  void _addLog({
    required String sensor,
    required String value,
    required String status,
    required String message,
    required bool isAlert,
  }) {
    final now = DateTime.now();
    final timestamp =
        '${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}';

    alertLogs.insert(
      0,
      _AlertLogEntry(
        timestamp: timestamp,
        sensor: sensor,
        value: value,
        status: status,
        message: message,
        isAlert: isAlert,
      ),
    );

    if (alertLogs.length > 30) {
      alertLogs.removeRange(30, alertLogs.length);
    }
  }

  void _showPhReminder() {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        behavior: SnackBarBehavior.floating,
        duration: Duration(seconds: 8),
        content: Text(
          'Reminder: Check water pH. Dip the sensor in the water after removing it from the 3N KCl solution.',
        ),
      ),
    );
  }

  Widget buildSensorCard(String title, String value, Color color) {
    return Expanded(
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        elevation: 2,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text(
                title,
                style: const TextStyle(fontSize: 14, color: Colors.grey),
              ),
              const SizedBox(height: 8),
              Text(
                value,
                style:
                    const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Container(
                height: 6,
                decoration: BoxDecoration(
                  color: color,
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget buildGraph(List<double> data, Color color) {
    if (data.isEmpty) {
      return const Center(child: Text('No data yet'));
    }

    return LineChart(
      LineChartData(
        gridData: const FlGridData(show: true),
        titlesData: const FlTitlesData(show: false),
        borderData: FlBorderData(show: true),
        lineBarsData: <LineChartBarData>[
          LineChartBarData(
            spots: List<FlSpot>.generate(
              data.length,
              (int i) => FlSpot(i.toDouble(), data[i]),
            ),
            isCurved: true,
            color: color,
            barWidth: 3,
            dotData: const FlDotData(show: false),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green[800],
        title: const Text('Smart Aquaponics Dashboard'),
        actions: <Widget>[
          Padding(
            padding: const EdgeInsets.only(right: 20),
            child: Row(
              children: <Widget>[
                Icon(
                  Icons.circle,
                  size: 12,
                  color: connected ? Colors.greenAccent : Colors.red,
                ),
                const SizedBox(width: 6),
                Text(
                  connected ? 'Connected' : 'Disconnected',
                  style: const TextStyle(fontSize: 14),
                ),
              ],
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Row(
              children: <Widget>[
                buildSensorCard(
                  'Water Level',
                  '${distance.toStringAsFixed(0)} cm',
                  Colors.blue,
                ),
                const SizedBox(width: 10),
                buildSensorCard('pH Level', ph.toStringAsFixed(1), Colors.orange),
                const SizedBox(width: 10),
                buildSensorCard(
                  'Temperature',
                  '${temperature.toStringAsFixed(1)} C',
                  Colors.red,
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: <Widget>[
                buildSensorCard(
                  'Last Feeding',
                  lastFeedingTime,
                  Colors.teal,
                ),
              ],
            ),
            const SizedBox(height: 30),
            const Text(
              'Sensor Readings',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            const Text('Water Level History'),
            SizedBox(height: 150, child: buildGraph(distanceHistory, Colors.blue)),
            const SizedBox(height: 20),
            const Text('Temperature History'),
            SizedBox(
              height: 150,
              child: buildGraph(temperatureHistory, Colors.red),
            ),
            const SizedBox(height: 25),
            const Text(
              'System Status',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              'Water Level: $waterLevelState (Low < ${lowWaterLevelCm.toStringAsFixed(0)} cm, High > ${highWaterLevelCm.toStringAsFixed(0)} cm)',
              style: const TextStyle(fontSize: 13, color: Colors.grey),
            ),
            const SizedBox(height: 8),
            Row(
              children: <Widget>[
                Expanded(
                  child: Card(
                    child: ListTile(
                      leading: const Icon(Icons.water),
                      title: const Text('Pump'),
                      subtitle: Text(pump1On ? 'ON' : 'OFF'),
                      trailing: Switch(
                        value: pump1On,
                        onChanged: null,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            const Text(
              'Alerts & Logs',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(10),
                child: Column(
                  children: alertLogs.isEmpty
                      ? <Widget>[
                          const ListTile(
                            leading: Icon(Icons.info_outline, color: Colors.grey),
                            title: Text('No logs yet'),
                          ),
                        ]
                      : alertLogs
                          .take(8)
                          .map(
                            (entry) => ListTile(
                              dense: true,
                              leading: Icon(
                                entry.isAlert ? Icons.error : Icons.check_circle,
                                color: entry.isAlert ? Colors.red : Colors.green,
                              ),
                              title: Text(
                                entry.isAlert
                                    ? 'ALERT: ${entry.message}'
                                    : entry.message,
                              ),
                              subtitle: Text(
                                '${entry.timestamp} | ${entry.sensor} | ${entry.value} | ${entry.status}',
                              ),
                            ),
                          )
                          .toList(),
                ),
              ),
            ),
            const SizedBox(height: 20),
            if (error.isNotEmpty)
              Text(
                'Error: $error',
                style: const TextStyle(color: Colors.grey),
              ),
          ],
        ),
      ),
    );
  }
}

class _SensorEval {
  const _SensorEval({
    required this.code,
    required this.logCode,
    required this.message,
    required this.isAlert,
  });

  final String code;
  final String logCode;
  final String message;
  final bool isAlert;
}

class _AlertLogEntry {
  const _AlertLogEntry({
    required this.timestamp,
    required this.sensor,
    required this.value,
    required this.status,
    required this.message,
    required this.isAlert,
  });

  final String timestamp;
  final String sensor;
  final String value;
  final String status;
  final String message;
  final bool isAlert;
}
