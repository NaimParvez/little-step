
# Violet Online Store

Violet Online Store is a Django-powered e-commerce platform designed for an intuitive and engaging online shopping experience. The project, developed as part of the Software Engineering Sessional (CSE 3206) course, features product browsing, user authentication, shopping cart management, and a rating/review system. This repository includes the full source code for the Violet Online Store, showcasing various functionalities such as product management, user interaction, and an admin dashboard.

## Features

- **Product Browsing**: Users can browse and filter products by category and price.
- **Cart Management**: Users can add/remove items to/from the shopping cart.
- **Rating and Review System**: Users can submit and view product reviews and ratings.
- **Admin Panel**: Admins can manage products, users, categories, featured items, coupons, and homepage sliders.
- **User Authentication**: Secure user registration, login, and password reset via a one-time email link.
- **Product Recommendations**: Basic product recommendation engine based on categories.

## Tech Stack

- **Backend**: Django 5.x (Python 3.10+)
- **Frontend**: Bootstrap 5, jQuery
- **Database**: SQLite (used during development)
- **Deployment**: Local Django development server (`runserver`)

## Installation

Follow these steps to set up the Violet Online Store on your local machine:

### Prerequisites

- Python 3.10+
- Django 5.x
- SQLite (comes by default with Django)

### Steps to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/NaimParvez/little-step.git
   ```

2. Navigate to the project directory:
   ```bash
   cd little-step
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser (admin) to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

9. Open your browser and navigate to `http://127.0.0.1:8000/` to view the website.

10. Access the admin panel at `http://127.0.0.1:8000/admin/` using the superuser credentials.

## Usage

- **Product Browsing**: Visit the homepage to browse products categorized by type.
- **Product Detail**: Click on any product to view detailed information, reviews, and ratings.
- **Rating and Review**: Users can submit a rating (1–5 stars) and write feedback for each product.
- **Cart Management**: Add items to your cart and proceed to checkout for simulated purchasing (payment integration is not yet implemented).
- **Admin Panel**: Admins can manage the products, users, and content via the Django admin interface.

## Screenshots

Here are some screenshots of the Violet Online Store:

- **Home Page**
  ![Home Page](./screenshots/home.png)

- **Login Page**
  ![Login Page](./screenshots/login.png)

- **Product Listing Page**
  ![Product Listing](./screenshots/products.png)

- **Admin Panel**
  ![Admin Panel](./screenshots/admin.png)

## Future Enhancements

The following features are planned for future development:

- **Real Payment Integration**: Adding payment gateways like bKash, SSLCommerz, etc.
- **AI-Powered Product Recommendation**: Enhancing the recommendation engine with machine learning models.
- **Order Tracking System**: Providing users with the ability to track their orders.
- **Email Marketing System**: Adding email notifications for promotional offers and order updates.
- **Advanced Analytics**: Providing admins with detailed analytics on user behavior, sales, etc.

## Contributing

Feel free to contribute by forking the repository and submitting a pull request with improvements or bug fixes.

### How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request and describe your changes.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For any questions, suggestions, or inquiries, feel free to contact me:

- **Md Naim Parvez**
- GitHub: [@NaimParvez](https://github.com/NaimParvez)
- Email: naimparvez99@outlook.com

```
