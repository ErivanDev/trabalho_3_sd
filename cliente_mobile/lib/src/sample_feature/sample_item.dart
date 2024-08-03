/// A placeholder class that represents an entity or model.
class Book {
  final int id;
  final String isbn;
  final String title;
  final String cover;
  final List<String> authors;
  final List<Review> reviews;

  Book({
    required this.id,
    required this.isbn,
    required this.title,
    required this.cover,
    required this.authors,
    required this.reviews,
  });

  factory Book.fromJson(Map<String, dynamic> json) {
    return Book(
      id: json['id'],
      isbn: json['isbn'],
      title: json['title'],
      cover: json['cover'],
      authors: List<String>.from(json['authors']),
      reviews: (json['reviews'] as List<dynamic>)
          .map((reviewJson) => Review.fromJson(reviewJson as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'isbn': isbn,
      'title': title,
      'cover': cover,
      'authors': authors,
      'reviews': reviews.map((review) => review.toJson()).toList(),
    };
  }
}

class Review {
  final int id;
  final String rating;
  final String reviewer;
  final String text;

  Review({
    required this.id,
    required this.rating,
    required this.reviewer,
    required this.text,
  });

  factory Review.fromJson(Map<String, dynamic> json) {
    return Review(
      id: json['id'],
      rating: json['rating'].toString(), // Ensure rating is a string
      reviewer: json['reviewer'],
      text: json['text'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'rating': rating,
      'reviewer': reviewer,
      'text': text,
    };
  }
}