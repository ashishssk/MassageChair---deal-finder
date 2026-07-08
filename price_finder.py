#!/usr/bin/env python3
"""
Price Tracker Script for OsakiUSA, OTAworld, and Shopify stores
Finds OSAKI and Titan brand massage chairs with 4D/3D features
Extracts prices, sorts by lowest price, and highlights discounts > 40%
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime
import re


class PriceTracker:
    def __init__(self):
        self.products = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_osaki_usa(self, collection_url):
        """Scrape products from OsakiUSA collection page"""
        print(f"\n🔍 Scraping OsakiUSA: {collection_url}")
        try:
            response = requests.get(collection_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product containers (adjust selectors based on actual site structure)
            products = soup.find_all('div', class_=['product-item', 'product-card', 'product'])
            
            for product in products:
                product_data = self._extract_product_info(product, 'OsakiUSA')
                if product_data:
                    self.products.append(product_data)
            
            print(f"✅ Found {len(self.products)} products from OsakiUSA")
        except Exception as e:
            print(f"❌ Error scraping OsakiUSA: {str(e)}")
    
    def scrape_ota_world(self, collection_url):
        """Scrape products from OTAworld collection page"""
        print(f"\n🔍 Scraping OTAworld: {collection_url}")
        try:
            response = requests.get(collection_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product containers
            products = soup.find_all('div', class_=['product-item', 'product-card', 'product'])
            
            for product in products:
                product_data = self._extract_product_info(product, 'OTAworld')
                if product_data:
                    self.products.append(product_data)
            
            print(f"✅ Found {len(self.products)} products from OTAworld")
        except Exception as e:
            print(f"❌ Error scraping OTAworld: {str(e)}")
    
    def scrape_shopify_store(self, collection_url):
        """Scrape products from Shopify store collection page"""
        print(f"\n🔍 Scraping Shopify store: {collection_url}")
        try:
            response = requests.get(collection_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Shopify product selectors
            products = soup.find_all('div', class_=['product-item', 'ProductCard'])
            
            for product in products:
                product_data = self._extract_product_info(product, 'Shopify')
                if product_data:
                    self.products.append(product_data)
            
            print(f"✅ Found {len(self.products)} products from Shopify")
        except Exception as e:
            print(f"❌ Error scraping Shopify store: {str(e)}")
    
    def _extract_product_info(self, product_elem, source):
        """Extract product name, price, and discount info"""
        try:
            # Extract product name
            name_elem = product_elem.find(['h2', 'h3', 'a'])
            name = name_elem.get_text(strip=True) if name_elem else "Unknown"
            
            # Check if product is OSAKI or Titan with 4D/3D features
            if not self._is_target_product(name):
                return None
            
            # Extract current price
            price_elem = product_elem.find(['span', 'div'], class_=['price', 'product-price'])
            price_text = price_elem.get_text(strip=True) if price_elem else None
            current_price = self._parse_price(price_text)
            
            if not current_price:
                return None
            
            # Extract original price (if on sale)
            original_price_elem = product_elem.find(['span', 'div'], class_=['original-price', 'compare-price'])
            original_price_text = original_price_elem.get_text(strip=True) if original_price_elem else None
            original_price = self._parse_price(original_price_text)
            
            # Calculate discount percentage
            discount_percent = 0
            if original_price and original_price > current_price:
                discount_percent = round(((original_price - current_price) / original_price) * 100, 1)
            
            # Extract product URL
            url_elem = product_elem.find('a', href=True)
            url = url_elem['href'] if url_elem else ""
            url = urljoin(source, url) if url else ""
            
            return {
                'name': name,
                'brand': self._extract_brand(name),
                'source': source,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'features': self._extract_features(name),
                'url': url,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"⚠️ Error extracting product info: {str(e)}")
            return None
    
    def _is_target_product(self, name):
        """Check if product is OSAKI or Titan brand with 4D/3D features"""
        name_lower = name.lower()
        
        # Check for brand
        has_brand = 'osaki' in name_lower or 'titan' in name_lower
        
        # Check for 4D or 3D features
        has_features = '4d' in name_lower or '3d' in name_lower
        
        return has_brand and has_features
    
    def _extract_brand(self, name):
        """Extract brand from product name"""
        name_lower = name.lower()
        if 'osaki' in name_lower:
            return 'OSAKI'
        elif 'titan' in name_lower:
            return 'Titan'
        return 'Unknown'
    
    def _extract_features(self, name):
        """Extract features from product name"""
        features = []
        name_lower = name.lower()
        
        if '4d' in name_lower:
            features.append('4D')
        if '3d' in name_lower:
            features.append('3D')
        if 'massage' in name_lower:
            features.append('Massage')
        if 'chair' in name_lower:
            features.append('Chair')
        
        return features
    
    def _parse_price(self, price_text):
        """Extract numerical price from text"""
        if not price_text:
            return None
        
        # Remove common currency symbols and extract numbers
        price_match = re.search(r'\$?[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group(0).replace('$', ''))
            except ValueError:
                return None
        return None
    
    def sort_by_price(self):
        """Sort products by lowest price first"""
        self.products.sort(key=lambda x: x['current_price'])
    
    def filter_high_discount(self, min_discount=40):
        """Filter products with discount >= min_discount percent"""
        return [p for p in self.products if p['discount_percent'] >= min_discount]
    
    def display_results(self):
        """Display formatted results"""
        if not self.products:
            print("\n❌ No products found!")
            return
        
        print("\n" + "="*100)
        print("💰 PRICE COMPARISON RESULTS - Sorted by Lowest Price")
        print("="*100)
        
        self.sort_by_price()
        
        for idx, product in enumerate(self.products, 1):
            label = "🎯 CHEAPEST DEAL" if idx == 1 else ""
            discount_label = "🔥 BIG DISCOUNT" if product['discount_percent'] >= 40 else ""
            
            print(f"\n{idx}. {product['name']}")
            print(f"   Brand: {product['brand']} | Features: {', '.join(product['features'])}")
            print(f"   💵 Current Price: ${product['current_price']:.2f}")
            
            if product['original_price']:
                print(f"   📌 Original Price: ${product['original_price']:.2f}")
                print(f"   📊 Discount: {product['discount_percent']}% OFF")
            
            print(f"   🛒 Source: {product['source']}")
            print(f"   🔗 URL: {product['url']}")
            
            if label:
                print(f"   ⭐ {label}")
            if discount_label:
                print(f"   ⭐ {discount_label}")
        
        print("\n" + "="*100)
        print(f"Total Products Found: {len(self.products)}")
        
        high_discount_products = self.filter_high_discount(40)
        if high_discount_products:
            print(f"Products with 40%+ Discount: {len(high_discount_products)}")
            print("\n🔥 HIGH DISCOUNT DEALS (40%+ OFF):")
            for product in high_discount_products:
                print(f"   • {product['name']} - {product['discount_percent']}% OFF (${product['current_price']:.2f})")
    
    def export_to_json(self, filename='price_comparison.json'):
        """Export results to JSON file"""
        self.sort_by_price()
        with open(filename, 'w') as f:
            json.dump(self.products, f, indent=2)
        print(f"\n✅ Results exported to {filename}")
    
    def export_to_csv(self, filename='price_comparison.csv'):
        """Export results to CSV file"""
        import csv
        self.sort_by_price()
        
        if not self.products:
            print("No products to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name', 'brand', 'source', 'current_price', 'original_price',
                'discount_percent', 'features', 'url'
            ])
            writer.writeheader()
            for product in self.products:
                product['features'] = '; '.join(product['features'])
                writer.writerow(product)
        
        print(f"\n✅ Results exported to {filename}")


def main():
    """Main execution"""
    tracker = PriceTracker()
    
    # Example URLs - Replace with actual collection page URLs
    osaki_url = "https://www.osakiusa.com/collections/massage-chairs"
    ota_world_url = "https://www.otaworld.com/collections/massage-chairs"
    shopify_url = "https://your-shopify-store.myshopify.com/collections/massage-chairs"
    
    # Scrape from all sources
    tracker.scrape_osaki_usa(osaki_url)
    tracker.scrape_ota_world(ota_world_url)
    tracker.scrape_shopify_store(shopify_url)
    
    # Display results
    tracker.display_results()
    
    # Export results
    tracker.export_to_json('price_comparison.json')
    tracker.export_to_csv('price_comparison.csv')


if __name__ == "__main__":
    main()
