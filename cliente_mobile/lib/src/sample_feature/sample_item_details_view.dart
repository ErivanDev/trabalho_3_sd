import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class SampleItemDetailsView extends StatefulWidget {
  const SampleItemDetailsView({super.key});

  static const routeName = '/sample_item';

  @override
  _SampleItemDetailsViewState createState() => _SampleItemDetailsViewState();
}

class _SampleItemDetailsViewState extends State<SampleItemDetailsView> {
  final TextEditingController _reviewTextController = TextEditingController();
  final TextEditingController _reviewRatingController= TextEditingController();
  final List<Map<String, dynamic>> _reviews = [];
  final String _isbn = '1467707376'; // Substitua pelo ISBN real

  @override
  void initState() {
    super.initState();
    _fetchReviews();
  }

  Future<void> _fetchReviews() async {
    // Fetch reviews from the server
    final response = await http.get(Uri.parse('http://localhost:5000/books/$_isbn/reviews'));
    
    if (response.statusCode == 200) {
      setState(() {
        _reviews.addAll(List<Map<String, dynamic>>.from(json.decode(response.body)));
      });
    } else {
      // Handle error
      print('Failed to load reviews');
    }
  }

  Future<void> _addReview() async {
    final reviewText = _reviewTextController.text;
    final reviewRating = _reviewRatingController.text;
    if (reviewText.isEmpty) return;

    final response = await http.post(
      Uri.parse('http://localhost:5000/books/$_isbn/reviews'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'text': reviewText, 'reviewer': "Anon", 'rating': reviewRating}),
    );

    if (response.statusCode == 201) {
      final newReview = json.decode(response.body);
      setState(() {
        _reviews.add(newReview);
      });
      _reviewTextController.clear();
      _reviewRatingController.clear();
    } else {
      // Handle error
      print('Failed to add review');
    }
  }

  Future<void> _deleteReview(int id) async {
    final response = await http.delete(
      Uri.parse('http://localhost:5000/books/$_isbn/reviews/$id'),
    );

    if (response.statusCode == 200) {
      setState(() {
        _reviews.removeWhere((review) => review['id'] == id);
      });
    } else {
      // Handle error
      print('Failed to delete review');
    }
  }

  Future<void> _updateReview(int id, String newText) async {
    final response = await http.put(
      Uri.parse('http://localhost:5000/books/$_isbn/reviews/$id'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'text': newText}),
    );

    if (response.statusCode == 200) {
      setState(() {
        final reviewIndex = _reviews.indexWhere((review) => review['id'] == id);
        if (reviewIndex != -1) {
          _reviews[reviewIndex]['text'] = newText;
        }
      });
    } else {
      // Handle error
      print('Failed to update review');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Item Details'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            TextField(
              controller: _reviewTextController,
              decoration: const InputDecoration(
                labelText: 'Add a review',
              ),
            ),
            const SizedBox(height: 8.0),
            TextField(
              controller: _reviewRatingController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Rating',
                hintText: 'Enter a rating (e.g., 4.5)',
              ),
            ),
            const SizedBox(height: 8.0),
            ElevatedButton(
              onPressed: _addReview,
              child: const Text('Submit Review'),
            ),
            const SizedBox(height: 16.0),
            Expanded(
              child: ListView.builder(
                itemCount: _reviews.length,
                itemBuilder: (context, index) {
                  final review = _reviews[index];
                  return ListTile(
                    title: Row(
                      children: [
                        Expanded(
                          child: Text(review['text']),
                        ),
                        Text('${review['rating']}'),
                      ],
                    ),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.edit),
                          onPressed: () async {
                            final newText = await _showEditDialog(review['text']);
                            if (newText != null && newText.isNotEmpty) {
                              _updateReview(review['id'], newText);
                            }
                          },
                        ),
                        IconButton(
                          icon: const Icon(Icons.delete),
                          onPressed: () => _deleteReview(review['id']),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<String?> _showEditDialog(String currentText) async {
    final TextEditingController _editController = TextEditingController(text: currentText);

    return showDialog<String>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Edit Review'),
          content: TextField(
            controller: _editController,
            decoration: const InputDecoration(
              labelText: 'Review',
            ),
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(_editController.text);
              },
              child: const Text('Save'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel'),
            ),
          ],
        );
      },
    );
  }
}
