import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../api_service.dart';
import 'package:intl/intl.dart'; // Import this package at the top

class TransactionHistoryPage extends StatefulWidget {
  @override
  _TransactionHistoryPageState createState() => _TransactionHistoryPageState();
}

class _TransactionHistoryPageState extends State<TransactionHistoryPage> {
  final storage = new FlutterSecureStorage();
  bool _isLoading = false;
  List<dynamic> _transactions = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchTransactionHistory();
  }

  Future<void> _fetchTransactionHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    String? token = await storage.read(key: 'jwt_token');

    final url = Uri.parse('${Config.baseUrl}/transaction-history/');
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      setState(() {
        _transactions = data;
      });
    } else {
      setState(() {
        _errorMessage = 'Failed to fetch transaction history';
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
        title: Text('Transaction History', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.blue.shade900,
      ),
      body: Container(
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
          child: _isLoading
              ? Center(child: CircularProgressIndicator())
              : _errorMessage != null
              ? Center(
            child: Text(
              _errorMessage!,
              style: TextStyle(color: Colors.red, fontSize: 18, fontWeight: FontWeight.bold),
            ),
          )
              : _transactions.isEmpty
              ? Center(
            child: Text(
              'No transactions available',
              style: TextStyle(color: Colors.white, fontSize: 18),
            ),
          )
              : ListView.builder(
            itemCount: _transactions.length,
            itemBuilder: (context, index) {
              var transaction = _transactions[index];
              DateTime dateTime = DateTime.parse(transaction['date']);
              String formattedDate = DateFormat('MMM. d, yyyy, h:mm a').format(dateTime);
              // String recipientName = transaction['recipient']['name'].toString();
              String recipientName = (transaction['recipient'] != null) ? (transaction['recipient']['name']): 'unkown';

              return Container(
                margin: EdgeInsets.symmetric(vertical: 8.0),
                padding: EdgeInsets.all(12.0),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.9),
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black12,
                      blurRadius: 4,
                      offset: Offset(0, 2),
                    ),
                  ],
                ),
                child: ListTile(
                  title: Text(
                    transaction['transaction_type'],
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                  ),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      SizedBox(height: 4),
                      Text(
                        'Amount: \$${transaction['amount']}',
                        style: TextStyle(fontSize: 16, color: Colors.black87),
                      ),
                      // if (transaction['recipient'] != null)
                        Text(
                          'Recipient: $recipientName',
                          style: TextStyle(fontSize: 14, color: Colors.black54),
                        ),
                      Text(
                        'Date: $formattedDate', // Use the formatted date,
                        style: TextStyle(fontSize: 14, color: Colors.black54),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
