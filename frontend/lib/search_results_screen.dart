// frontend/lib/search_results_screen.dart
import 'package:flutter/material.dart';
import 'api_service.dart';
import 'product_model.dart';

class SearchResultsScreen extends StatelessWidget {
  final String searchQuery;
  final String? sortBy;

  SearchResultsScreen({required this.searchQuery, this.sortBy});

  final ApiService _apiService = ApiService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Search Results'),
      ),
      body: FutureBuilder<List<Product>>(
        future: _apiService.getProducts(
          search: searchQuery,
          sortBy: sortBy,
        ),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No products found'));
          } else {
            final products = snapshot.data!;
            return ListView.builder(
              itemCount: products.length,
              itemBuilder: (context, index) {
                final product = products[index];
                return ListTile(
                  title: Text(product.name),
                  subtitle: Text('\$${product.price}'),
                );
              },
            );
          }
        },
      ),
    );
  }
}