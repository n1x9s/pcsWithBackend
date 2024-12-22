import 'package:flutter/material.dart';
import 'api_service.dart';

class ProfileScreen extends StatelessWidget {
  final ApiService apiService;

  ProfileScreen({required this.apiService});

  void _handle401Error(BuildContext context) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Session expired. Please log in again.')),
      );
      Navigator.pushReplacementNamed(context, '/login');
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>?>(
      future: apiService.getUserProfile(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Scaffold(
            appBar: AppBar(title: Text('Profile')),
            body: Center(child: CircularProgressIndicator()),
          );
        } else if (snapshot.hasError) {
          final error = snapshot.error.toString();
          print('Profile error: $error'); // Отладка
          if (error.contains('401')) {
            _handle401Error(context);
          }
          return Scaffold(
            appBar: AppBar(title: Text('Profile')),
            body: Center(
              child: Text('Error: Unable to fetch profile data'),
            ),
          );
        } else if (snapshot.hasData) {
          final user = snapshot.data!;
          return Scaffold(
            appBar: AppBar(title: Text('Profile')),
            body: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Full Name: ${user['name']}', style: TextStyle(fontSize: 18)),
                  SizedBox(height: 8),
                  Text('Email: ${user['email']}', style: TextStyle(fontSize: 18)),
                  ElevatedButton(
                    onPressed: () async {
                      await apiService.logout();
                      Navigator.pushReplacementNamed(context, '/login');
                    },
                    child: Text('Logout'),
                  ),
                ],
              ),
            ),
          );
        } else {
          return Scaffold(
            appBar: AppBar(title: Text('Profile')),
            body: Center(
              child: Text('No profile data available'),
            ),
          );
        }
      },
    );
  }
}
