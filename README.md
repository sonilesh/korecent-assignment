### Korecent

Custom App for following functionalities:

1. Generate PO automatically when SO is submitted with supplier in item child table entries.

2. API for inserting Sales orders in erpnext with and without master data of customer and items in erpnext.
Note: Create master data if it doesn't exists.

API Endpoint: /api/method/korecent.korecent.api.v1.create_sales_order
Sample Payload: {
    "customer": "CUST-003",
    "items": [
        {
            "item_name": "Item D",
            "qty": 100,
            "rate": 100,
            "delivery_date": "30-04-2024"
        },
        {
            "item_name": "Headphones",
            "qty": 300,
            "rate": 200,
            "delivery_date": "30-04-2024"
        }
    ]
}
Sample Response: {
    "status": "success",
    "data": {
        "sales_order": "SAL-ORD-2024-00001"
    },
    "error": {
        "message": "",
        "traceback": ""
    }
}
Note: Use Authorization token in headers with API Key and Secret to hit the API.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app korecent
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/korecent
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
