class Product {
  final int id;
  final String name;
  final String description;
  final double price;
  final String imageUrl; // Новое поле для изображения

  Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.imageUrl, // Новое поле для изображения
  });

  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'] ?? 0, // Убедитесь, что id не равен null
      name: json['name'] ?? 'Unknown', // Убедитесь, что name не равен null
      description: json['description'] ?? 'No description', // Убедитесь, что description не равен null
      price: (json['price'] != null) ? json['price'].toDouble() : 0.0, // Убедитесь, что price не равен null
      imageUrl: json['image_url'] ?? '', // Убедитесь, что imageUrl не равен null
    );
  }
}