import json
import csv

# Function to calculate total value of an item (price * quantity)
def calculate_total_value(price, quantity):
    return price * quantity

# Function to calculate the discount (10% if the total value exceeds $100)
def calculate_discount(total_value):
    return total_value * 0.10 if total_value > 100 else 0

# Function to calculate shipping cost (e.g., $5 per item)
def calculate_shipping_cost(quantity):
    return 5 * quantity

# Function to process the data and restructure it
def process_order_data(file_path):
    # Read the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)

    # List to store all processed data for CSV
    processed_data = []

    # Iterate through orders
    for order in data['orders']:
        order_id = order['order_id']
        customer_name = order['customer']['name']
        shipping_address = order['shipping_address']
        
        # Iterate through items in each order
        for item in order['items']:
            product_name = item['name']
            product_price = item['price']
            quantity_purchased = item['quantity']
            
            # Calculate total value, discount, shipping cost, and final total
            total_value = calculate_total_value(product_price, quantity_purchased)
            discount = calculate_discount(total_value)
            shipping_cost = calculate_shipping_cost(quantity_purchased)
            final_total = total_value - discount + shipping_cost

            # Extract country code from shipping address (as an example, using the state code)
            # Assuming the last part of the shipping address contains the state or country code
            country_code = shipping_address.split(',')[-1].strip().split()[-1]

            # Append the processed order data to the list
            processed_data.append([
                order_id,
                customer_name,
                product_name,
                product_price,
                quantity_purchased,
                total_value,
                discount,
                shipping_cost,
                final_total,
                shipping_address,
                country_code
            ])

    return processed_data

# Function to write the processed data into a CSV file
def write_to_csv(processed_data, output_file):
    # Define the header for the CSV file
    header = ['Order ID', 'Customer Name', 'Product Name', 'Product Price', 'Quantity Purchased', 
              'Total Value', 'Discount', 'Shipping Cost', 'Final Total', 'Shipping Address', 'Country Code']

    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(processed_data)

# Function to sort orders by the final total amount spent by each customer
def sort_by_final_total(processed_data):
    return sorted(processed_data, key=lambda x: x[-2], reverse=True)

# Main function
def main():
    input_file = '.sales.json'  # Path to the input JSON file
    output_file = '/orders.csv'  # Path to the output CSV file

    # Process the data and generate the list
    processed_data = process_order_data(input_file)

    # Sort the data by the final total amount spent by each customer
    sorted_data = sort_by_final_total(processed_data)

    # Write the sorted data to CSV
    write_to_csv(sorted_data, output_file)

    print(f"Data has been processed and saved to {output_file}")

if __name__ == "__main__":
    main()
