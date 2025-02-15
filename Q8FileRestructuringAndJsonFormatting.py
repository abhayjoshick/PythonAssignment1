import json
import csv

def calculate_total_value(price, quantity):
    return price * quantity

def calculate_discount(total_value):
    return total_value * 0.10 if total_value > 100 else 0

def calculate_shipping_cost(quantity):
    return 5 * quantity

def process_order_data(file_path):

    with open(file_path, 'r') as f:
        data = json.load(f)

    processed_data = []

    for order in data['orders']:
        order_id = order['order_id']
        customer_name = order['customer']['name']
        shipping_address = order['shipping_address']
        
        for item in order['items']:
            product_name = item['name']
            product_price = item['price']
            quantity_purchased = item['quantity']
            
            total_value = calculate_total_value(product_price, quantity_purchased)
            discount = calculate_discount(total_value)
            shipping_cost = calculate_shipping_cost(quantity_purchased)
            final_total = total_value - discount + shipping_cost

            country_code = shipping_address.split(',')[-1].strip().split()[-1]

           
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

def write_to_csv(processed_data, output_file):
    header = ['Order ID', 'Customer Name', 'Product Name', 'Product Price', 'Quantity Purchased', 
              'Total Value', 'Discount', 'Shipping Cost', 'Final Total', 'Shipping Address', 'Country Code']

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(processed_data)

def sort_by_final_total(processed_data):
    return sorted(processed_data, key=lambda x: x[-2], reverse=True)

def main():
    input_file = '/home/abhay/python/PythonAssignment1/sales.json' 
    output_file = '/home/abhay/python/PythonAssignment1/orders.csv'  
    processed_data = process_order_data(input_file)

    sorted_data = sort_by_final_total(processed_data)

    write_to_csv(sorted_data, output_file)

    print(f"Data has been processed and saved to {output_file}")

if __name__ == "__main__":
    main()
