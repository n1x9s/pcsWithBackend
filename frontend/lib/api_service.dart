import 'package:dio/dio.dart';
import 'product_model.dart';

class ApiService {
  final Dio _dio = Dio();
  String? _authToken;

  // Установка токена
  void setAuthToken(String token) {
    _authToken = token;
    _dio.options.headers['Authorization'] = 'Bearer $token';
    print('Authorization header set: Bearer $token'); // Отладка
  }


  // Очистка токена
  void clearAuthToken() {
    _authToken = null;
    _dio.options.headers.remove('Authorization');
    print('Authorization header cleared');
  }

  // Логин
  Future<String?> login(String email, String password) async {
    try {
      final response = await _dio.post(
        'http://127.0.0.1:8000/auth/login',
        data: {'email': email, 'password': password},
      );
      if (response.statusCode == 200) {
        final token = response.data['access_token'];
        setAuthToken(token);
        return token;
      } else {
        throw Exception('Failed to log in');
      }
    } catch (e) {
      throw Exception('Error during login: $e');
    }
  }

  // Регистрация
  Future<void> register(String email, String password) async {
    try {
      final response = await _dio.post(
        'http://127.0.0.1:8000/auth/register',
        data: {'email': email, 'password': password},
      );
      if (response.statusCode == 201) {
        print('Registration successful');
      } else {
        throw Exception('Failed to register');
      }
    } catch (e) {
      throw Exception('Error during registration: $e');
    }
  }

  // Выход
  Future<void> logout() async {
    try {
      await _dio.post('http://127.0.0.1:8000/auth/logout');
      clearAuthToken();
    } catch (e) {
      throw Exception('Error during logout: $e');
    }
  }

  // Получение профиля
  Future<Map<String, dynamic>?> getUserProfile() async {
    if (_authToken == null || _authToken!.isEmpty) {
      throw Exception('No token available');
    }
    try {
      final response = await _dio.get('http://127.0.0.1:8000/users/me');
      return response.data;
    } catch (e) {
      throw Exception('Error fetching user profile: $e');
    }
  }

  // Получение продуктов
  Future<List<Product>> getProducts({String? search, String? sortBy}) async {
    try {
      final queryParams = <String, dynamic>{};
      if (search != null) queryParams['search'] = search;
      if (sortBy != null) queryParams['sort_by'] = sortBy;

      final response = await _dio.get(
        'http://127.0.0.1:8000/products/',
        queryParameters: queryParams,
      );

      if (response.statusCode == 200) {
        List<Product> products = (response.data as List)
            .map((product) => Product.fromJson(product))
            .toList();
        return products;
      } else {
        throw Exception('Failed to load products');
      }
    } catch (e) {
      throw Exception('Error fetching products: $e');
    }
  }

  // Отправка сообщения
  Future<void> sendMessage(int receiverId, String message) async {
    try {
      final response = await _dio.post(
        'http://127.0.0.1:8000/chat/send/$receiverId',
        data: {'message': message},
      );
      if (response.statusCode != 200) {
        throw Exception('Failed to send message');
      }
    } catch (e) {
      throw Exception('Error sending message: $e');
    }
  }
  bool isTokenValid() {
    return _authToken != null && _authToken!.isNotEmpty;
  }

  // Получение сообщений
  Future<List<Map<String, dynamic>>> getMessages(int otherUserId) async {
    if (_authToken == null || _authToken!.isEmpty) {
      throw Exception('No token available. Please log in again.');
    }
    try {
      print('Headers: ${_dio.options.headers}');
      final response = await _dio.get(
        'http://127.0.0.1:8000/chat/messages/$otherUserId',
      );
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(response.data);
      } else {
        throw Exception('Failed to fetch messages: ${response.statusMessage}');
      }
    } catch (e) {
      throw Exception('Error fetching messages: $e');
    }
  }
}
