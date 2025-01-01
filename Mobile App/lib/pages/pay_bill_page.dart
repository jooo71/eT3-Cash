import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:wallet/api_service.dart';

class PayBillPage extends StatefulWidget {
  @override
  _PayBillPageState createState() => _PayBillPageState();
}

class _PayBillPageState extends State<PayBillPage> {
  final _amountController = TextEditingController();
  final storage = new FlutterSecureStorage();
  bool _isLoading = false;
  String? _successMessage;
  String? _errorMessage;
  String? _selectedBillType;

  // List of available bills
  final List<String> _billTypes = [
    'Electricity',
    'Water',
    'Internet',
    'Gas',
  ];

  Future<void> _payBill() async {
    setState(() {
      _isLoading = true;
      _successMessage = null;
      _errorMessage = null;
    });

    String? token = await storage.read(key: 'jwt_token');
    final amount = _amountController.text;

    final url = Uri.parse('${Config.baseUrl}/pay-bill/');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(<String, String>{
        'amount': amount,
        'bill_type': _selectedBillType!,  // Sending the selected bill type
      }),
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      setState(() {
        _successMessage = data['message'];
      });
    } else {
      setState(() {
        _errorMessage = 'Payment failed';
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;

    return Scaffold(
      appBar: AppBar(
        title: Text('Pay Bill', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.blue.shade900,
      ),
      body: SingleChildScrollView(
        child: Container(
          width: width,
          height: height,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [Colors.blue.shade900, Colors.blue.shade100],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Dropdown for bill type
                DropdownButtonFormField<String>(
                  decoration: InputDecoration(
                    filled: true,
                    fillColor: Colors.white,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    hintText: 'Select Bill Type',
                  ),
                  value: _selectedBillType,
                  items: _billTypes.map((String bill) {
                    return DropdownMenuItem<String>(
                      value: bill,
                      child: Text(bill),
                    );
                  }).toList(),
                  onChanged: (newValue) {
                    setState(() {
                      _selectedBillType = newValue;
                    });
                  },
                ),
                SizedBox(height: 16),
                // TextField for amount input
                TextField(
                  controller: _amountController,
                  decoration: InputDecoration(
                    hintText: 'Amount',
                    labelStyle: TextStyle(color: Colors.white),
                    filled: true,
                    fillColor: Colors.white.withOpacity(1),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                  keyboardType: TextInputType.number,
                  style: TextStyle(color: Colors.black),
                ),
                SizedBox(height: 16),
                // Payment button
                _isLoading
                    ? const CircularProgressIndicator()
                    : ElevatedButton(
                  onPressed: _payBill,
                  style: ElevatedButton.styleFrom(
                    primary: Colors.blue.shade900, // Button color
                    padding: EdgeInsets.symmetric(
                      horizontal: 50,
                      vertical: 15,
                    ),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: Text(
                    'Pay Bill',
                    style: TextStyle(fontSize: 18, color: Colors.white),
                  ),
                ),
                if (_successMessage != null) ...[
                  SizedBox(height: 16),
                  Text(
                    _successMessage!,
                    style: TextStyle(color: Color(0xFF062806), fontSize: 20),
                  ),
                ],
                if (_errorMessage != null) ...[
                  SizedBox(height: 16),
                  Text(
                    _errorMessage!,
                    style: TextStyle(color: Colors.red, fontSize: 16),
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
