# 🗄️ Nexus Tech Store - Database Architecture & Schema Specification

This document details the relational database design, table relationships, foreign key constraints, and indexing strategies for the **Nexus Tech Store** Django REST Framework backend.

---

## 📊 Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER ||--o{ REVIEW : writes
    USER ||--o{ WISHLIST : favorites
    USER ||--o{ CART_ITEM : owns

    CATEGORY ||--o{ PRODUCT : categorizes
    PRODUCT ||--o{ PRODUCT_VARIANT : has
    PRODUCT ||--o{ REVIEW : receives
    PRODUCT ||--o{ WISHLIST : favorited_in
    PRODUCT ||--o{ ORDER_ITEM : ordered_as
    PRODUCT ||--o{ CART_ITEM : added_to

    PRODUCT_VARIANT ||--o{ ORDER_ITEM : specified_as
    PRODUCT_VARIANT ||--o{ CART_ITEM : selected_in

    ORDER ||--|{ ORDER_ITEM : contains

    USER {
        int id PK
        string username UK
        string email UK
        string name
        string role "customer | admin"
        string country
        string avatar_url
    }

    CATEGORY {
        int id PK
        string name
        string slug UK
        string icon
        string description
        datetime created_at
    }

    PRODUCT {
        int id PK
        int category_id FK
        string name
        decimal price
        text description
        json specs
        int stock_qty
        string image_url
        string brand
        boolean is_featured
        boolean is_new
        float rating
        int num_reviews
        datetime created_at
    }

    PRODUCT_VARIANT {
        int id PK
        int product_id FK
        string color_name
        string hex_code
        string image_url
        decimal price_delta
        int stock_qty
        boolean is_default
    }

    REVIEW {
        int id PK
        int product_id FK
        int user_id FK
        int rating "1 to 5"
        text comment
        datetime created_at
        datetime updated_at
    }

    ORDER {
        int id PK
        int user_id FK
        string status "pending | processing | shipped | delivered | cancelled"
        decimal total_amount
        decimal shipping_cost
        text shipping_address
        string city
        string postal_code
        string country
        string payment_method
        string payment_status "unpaid | paid | refunded"
        string tracking_number
        text notes
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int variant_id FK
        string product_name_snapshot
        string variant_name_snapshot
        int quantity
        decimal price_at_purchase
    }

    CART_ITEM {
        int id PK
        int user_id FK
        int product_id FK
        int variant_id FK
        int quantity
        datetime created_at
        datetime updated_at
    }

    WISHLIST {
        int id PK
        int user_id FK
        int product_id FK
        datetime created_at
    }
```

---

## 🔑 Key Invariants & Safeguards

1. **Snapshot Pricing & Naming**:
   - `OrderItem` preserves `price_at_purchase`, `product_name_snapshot`, and `variant_name_snapshot` at the exact checkout timestamp, making past invoices immutable to future product price adjustments.

2. **Automated Rating Re-aggregation**:
   - Creating, modifying, or deleting a `Review` automatically triggers `Product.update_rating()` to compute real-time average stars and total count.

3. **Compound Unique Constraints**:
   - `Review`: `unique_together = ('product', 'user')` - prevents duplicate reviews from the same account.
   - `Wishlist`: `unique_together = ('user', 'product')` - avoids redundant bookmarking.
