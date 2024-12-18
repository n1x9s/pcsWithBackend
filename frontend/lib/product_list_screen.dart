// frontend/lib/product_list_screen.dart
import 'package:flutter/material.dart';
import 'api_service.dart';
import 'product_model.dart';
import 'search_results_screen.dart';

class ProductListScreen extends StatefulWidget {
  @override
  _ProductListScreenState createState() => _ProductListScreenState();
}

class _ProductListScreenState extends State<ProductListScreen> {
  final ApiService _apiService = ApiService();
  String? _searchQuery;
  String? _sortBy;
  final TextEditingController _searchController = TextEditingController();

  void _onSearchChanged(String query) {
    setState(() {
      _searchQuery = query;
    });
  }

  void _onSortChanged(String? sortBy) {
    setState(() {
      _sortBy = sortBy;
    });
  }

  void _navigateToSearch() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => SearchResultsScreen(
          searchQuery: _searchController.text,
          sortBy: _sortBy,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Products'),
        actions: [
          IconButton(
            icon: Icon(Icons.search),
            onPressed: _navigateToSearch,
          ),
          PopupMenuButton<String>(
            onSelected: _onSortChanged,
            itemBuilder: (context) => [
              PopupMenuItem(
                value: 'price_asc',
                child: Text('Sort by Price (Asc)'),
              ),
              PopupMenuItem(
                value: 'price_desc',
                child: Text('Sort by Price (Desc)'),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'Enter product name',
                border: OutlineInputBorder(),
              ),
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Product>>(
              future: _apiService.getProducts(
                search: _searchQuery,
                sortBy: _sortBy,
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
          ),
        ],
      ),
    );
  }
}