import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../api_service.dart';

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _phoneController = TextEditingController();
  final _nameController = TextEditingController();
  final _passwordController = TextEditingController();

  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;

  Future<void> _register() async {
    if (_phoneController.text.isEmpty ||
        _nameController.text.isEmpty ||
        _passwordController.text.isEmpty) {
      setState(() {
        _errorMessage = 'Please fill in all fields.';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
    });

    final phoneNumber = _phoneController.text;
    final name = _nameController.text;
    final password = _passwordController.text;

    final url = Uri.parse('${Config.baseUrl}/register/');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'phone_number': phoneNumber,
        'name': name,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      setState(() {
        _successMessage = 'Registration successful! You can now log in.';
      });
    } else {
      setState(() {
        _errorMessage = 'Registration failed. Please try again.';
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    // Get the screen height and width using MediaQuery
    final mediaQuery = MediaQuery.of(context);
    final screenHeight = mediaQuery.size.height;
    final screenWidth = mediaQuery.size.width;

    // Check device orientation
    final isPortrait = mediaQuery.orientation == Orientation.portrait;

    // Set icon size based on orientation
    final iconSize = isPortrait ? screenHeight * 0.15 : screenHeight * 0.31;
    final buttonsize = isPortrait ?  screenHeight * 0.07 : screenHeight * 0.17; // second number is portrait number
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.blue.shade900,
      ),
      resizeToAvoidBottomInset: true,
      body: Container(
        height: screenHeight,
        width: screenWidth,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade900, Colors.blue.shade100],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: SingleChildScrollView(
          child: Padding(
            padding: EdgeInsets.all(screenWidth * 0.05), // 5% padding
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SizedBox(height: screenHeight * 0.1),
                Icon(
                  Icons.app_registration,
                  size: iconSize, // Set icon size based on orientation
                  color: Colors.blue[900],
                ),
                SizedBox(height: screenHeight * 0.1), // 10% of screen height
                TextField(
                  controller: _phoneController,
                  decoration: InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    filled: true,
                    fillColor: Colors.grey.shade50,
                    hintText: 'Phone Number',
                    hintStyle: TextStyle(
                      color: Colors.grey.shade700,
                      fontSize: 15,
                    ),
                    prefixIcon: const Icon(Icons.phone),
                  ),
                  keyboardType: TextInputType.phone,
                ),
                SizedBox(height: screenHeight * 0.02), // 2% of screen height
                TextField(
                  controller: _nameController,
                  decoration: InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    filled: true,
                    fillColor: Colors.grey.shade50,
                    hintText: 'Name',
                    hintStyle: TextStyle(
                      color: Colors.grey.shade700,
                      fontSize: 15,
                    ),
                    prefixIcon: const Icon(Icons.abc_sharp, size: 30),
                  ),
                ),
                SizedBox(height: screenHeight * 0.02),
                TextField(
                  controller: _passwordController,
                  decoration: InputDecoration(
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(80.0),
                      borderSide: const BorderSide(color: Colors.black),
                    ),
                    filled: true,
                    fillColor: Colors.grey.shade50,
                    hintText: 'Password',
                    hintStyle: TextStyle(
                      color: Colors.grey.shade700,
                      fontSize: 15,
                    ),
                    prefixIcon: const Icon(Icons.password_outlined, size: 30),
                  ),
                  obscureText: true,
                ),
                SizedBox(height: screenHeight * 0.02),
                if (_isLoading)
                  CircularProgressIndicator()
                else
                  SizedBox(
                    width: screenWidth * 0.5, // 50% of screen width
                    height: buttonsize, // 7% of screen height
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        primary: Colors.blue[900],
                      ),
                      onPressed: _register,
                      child: Text('Register', style: TextStyle(color: Colors.white)),
                    ),
                  ),
                if (_successMessage != null) ...[
                  SizedBox(height: screenHeight * 0.02),
                  Text(
                    _successMessage!,
                    style: TextStyle(color: Color(0xFF062806), fontSize: 20),
                  ),
                ],
                if (_errorMessage != null) ...[
                  SizedBox(height: screenHeight * 0.02),
                  Text(
                    _errorMessage!,
                    style: TextStyle(color: Colors.red),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
