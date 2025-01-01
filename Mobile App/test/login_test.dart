import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:wallet/api_service.dart';

class MockClient extends Mock implements http.Client {}

void main() {
  group('LoginPage Tests', () {
    test('Successful login', () async {
      // Mock HTTP client
      final client = MockClient();
      final phoneNumber = '0123456789';
      final password = 'testpass';

      // Set up mock response
      when(client.post(
        Uri.parse('${Config.baseUrl}/login/'),
        headers: anyNamed('headers'),
        body: jsonEncode({'phone_number': phoneNumber, 'password': password}),
      )).thenAnswer((_) async => http.Response('{"access": "fake_token"}', 200));

      // Call your login method and check for results
    });
  });
}
