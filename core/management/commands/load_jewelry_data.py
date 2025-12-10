from django.core.management.base import BaseCommand
from products.models import Product
from customers.models import Customer


class Command(BaseCommand):
    help = 'Loads dummy jewelry data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Loading jewelry store data...'))
        
        # Create Jewelry Products
        products_data = [
            # Gold Jewelry
            {'sku': 'GR001', 'name': 'Gold Ring 18K', 'category': 'Gold Rings', 'cost_price': 450, 'selling_price': 650, 'stock_quantity': 25},
            {'sku': 'GR002', 'name': 'Gold Ring 21K', 'category': 'Gold Rings', 'cost_price': 550, 'selling_price': 800, 'stock_quantity': 15},
            {'sku': 'GN001', 'name': 'Gold Necklace 18K', 'category': 'Gold Necklaces', 'cost_price': 1200, 'selling_price': 1750, 'stock_quantity': 12},
            {'sku': 'GN002', 'name': 'Gold Chain 21K', 'category': 'Gold Necklaces', 'cost_price': 1500, 'selling_price': 2200, 'stock_quantity': 8},
            {'sku': 'GB001', 'name': 'Gold Bracelet 18K', 'category': 'Gold Bracelets', 'cost_price': 800, 'selling_price': 1200, 'stock_quantity': 18},
            {'sku': 'GE001', 'name': 'Gold Earrings 18K', 'category': 'Gold Earrings', 'cost_price': 350, 'selling_price': 550, 'stock_quantity': 30},
            
            # Diamond Jewelry
            {'sku': 'DR001', 'name': 'Diamond Ring 0.5ct', 'category': 'Diamond Rings', 'cost_price': 2500, 'selling_price': 3800, 'stock_quantity': 5},
            {'sku': 'DR002', 'name': 'Diamond Ring 1ct', 'category': 'Diamond Rings', 'cost_price': 5000, 'selling_price': 7500, 'stock_quantity': 3},
            {'sku': 'DN001', 'name': 'Diamond Necklace', 'category': 'Diamond Necklaces', 'cost_price': 3500, 'selling_price': 5200, 'stock_quantity': 4},
            {'sku': 'DE001', 'name': 'Diamond Earrings', 'category': 'Diamond Earrings', 'cost_price': 1800, 'selling_price': 2700, 'stock_quantity': 7},
            
            # Silver Jewelry
            {'sku': 'SR001', 'name': 'Silver Ring 925', 'category': 'Silver Rings', 'cost_price': 45, 'selling_price': 80, 'stock_quantity': 50},
            {'sku': 'SN001', 'name': 'Silver Necklace 925', 'category': 'Silver Necklaces', 'cost_price': 85, 'selling_price': 150, 'stock_quantity': 35},
            {'sku': 'SB001', 'name': 'Silver Bracelet 925', 'category': 'Silver Bracelets', 'cost_price': 60, 'selling_price': 110, 'stock_quantity': 40},
            
            # Pearl Jewelry
            {'sku': 'PN001', 'name': 'Pearl Necklace', 'category': 'Pearl Jewelry', 'cost_price': 450, 'selling_price': 750, 'stock_quantity': 10},
            {'sku': 'PE001', 'name': 'Pearl Earrings', 'category': 'Pearl Jewelry', 'cost_price': 200, 'selling_price': 350, 'stock_quantity': 20},
            
            # Wedding Sets
            {'sku': 'WS001', 'name': 'Wedding Ring Set 18K', 'category': 'Wedding Sets', 'cost_price': 1200, 'selling_price': 1850, 'stock_quantity': 6},
            {'sku': 'WS002', 'name': 'Engagement Ring Set', 'category': 'Wedding Sets', 'cost_price': 3000, 'selling_price': 4500, 'stock_quantity': 4},
            
            # Low Stock Items
            {'sku': 'GR003', 'name': 'Gold Ring 22K Premium', 'category': 'Gold Rings', 'cost_price': 750, 'selling_price': 1100, 'stock_quantity': 2},
            {'sku': 'DR003', 'name': 'Diamond Pendant', 'category': 'Diamond Pendants', 'cost_price': 2200, 'selling_price': 3300, 'stock_quantity': 1},
        ]

        created_products = 0
        for data in products_data:
            _, created = Product.objects.get_or_create(sku=data['sku'], defaults=data)
            if created:
                created_products += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_products} new products ({len(products_data)} total)'))

        # Create Jewelry Store Customers
        customers_data = [
            {'customer_id': 'JC001', 'name': 'Ahmed Hassan', 'phone': '010-1234-5678', 'email': 'ahmed.hassan@gmail.com', 'address': '15 El Tahrir Street, Dokki, Cairo', 'opening_balance': 0},
            {'customer_id': 'JC002', 'name': 'Fatima Khalil', 'phone': '011-2345-6789', 'email': 'fatima.khalil@gmail.com', 'address': '42 Salah Salem Road, Nasr City, Cairo', 'opening_balance': 1500},
            {'customer_id': 'JC003', 'name': 'Mohamed Ali', 'phone': '012-3456-7890', 'email': 'mohamed.ali@hotmail.com', 'address': '88 El Horreya Avenue, Alexandria', 'opening_balance': 0},
            {'customer_id': 'JC004', 'name': 'Mona Ibrahim', 'phone': '010-4567-8901', 'email': 'mona.ibrahim@yahoo.com', 'address': '23 Road 9, Maadi, Cairo', 'opening_balance': 500},
            {'customer_id': 'JC005', 'name': 'Omar Mostafa', 'phone': '011-5678-9012', 'email': 'omar.mostafa@gmail.com', 'address': '56 El Merghany Street, Heliopolis, Cairo', 'opening_balance': 0},
            {'customer_id': 'JC006', 'name': 'Noha Samir', 'phone': '012-6789-0123', 'email': 'noha.samir@gmail.com', 'address': '34 El Thawra Street, Giza', 'opening_balance': 2000},
            {'customer_id': 'JC007', 'name': 'Amr Abdel Rahman', 'phone': '010-7890-1234', 'email': 'amr.abdelrahman@outlook.com', 'address': '12 Mohamed Farid Street, Downtown Cairo', 'opening_balance': 0},
            {'customer_id': 'JC008', 'name': 'Laila Mahmoud', 'phone': '011-8901-2345', 'email': 'laila.mahmoud@gmail.com', 'address': '78 El Hegaz Street, Heliopolis, Cairo', 'opening_balance': 1000},
            {'customer_id': 'JC009', 'name': 'Khaled Youssef', 'phone': '012-9012-3456', 'email': 'khaled.youssef@gmail.com', 'address': '45 Stanley Bridge, Alexandria', 'opening_balance': 0},
            {'customer_id': 'JC010', 'name': 'Sara Gamal', 'phone': '010-0123-4567', 'email': 'sara.gamal@hotmail.com', 'address': '67 Road 216, Degla, Maadi, Cairo', 'opening_balance': 750},
            {'customer_id': 'JC011', 'name': 'Youssef Nabil', 'phone': '011-1234-5670', 'email': 'youssef.nabil@gmail.com', 'address': '90 Makram Ebeid Street, Nasr City, Cairo', 'opening_balance': 0},
            {'customer_id': 'JC012', 'name': 'Heba Fouad', 'phone': '012-2345-6701', 'email': 'heba.fouad@yahoo.com', 'address': '33 El Orouba Street, Heliopolis, Cairo', 'opening_balance': 1200},
        ]

        created_customers = 0
        for data in customers_data:
            _, created = Customer.objects.get_or_create(customer_id=data['customer_id'], defaults=data)
            if created:
                created_customers += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_customers} new customers ({len(customers_data)} total)'))

        self.stdout.write(self.style.SUCCESS('\n✅ Jewelry store data loaded successfully!'))
        self.stdout.write('   - Gold, Diamond, Silver, Pearl, and Wedding jewelry')
        self.stdout.write('   - Some items with low stock for testing alerts')
