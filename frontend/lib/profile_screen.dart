import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  final String fullName;
  final String phoneNumber;
  final String email;

  ProfileScreen({
    required this.fullName,
    required this.phoneNumber,
    required this.email,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Profile'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Full Name: $fullName', style: TextStyle(fontSize: 18)),
            SizedBox(height: 8),
            Text('Phone Number: $phoneNumber', style: TextStyle(fontSize: 18)),
            SizedBox(height: 8),
            Text('Email: $email', style: TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
