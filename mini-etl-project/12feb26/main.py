

raw_data = [
    {"tx_id": "TXN-001", "date": "2023-10-01", "product": "  Laptop Gaming ", "price": "15000000", "qty": 1},
    {"tx_id": "TXN-002", "date": "2023-10-01", "product": "Mouse Wireless", "price": "150000", "qty": 2},
    {"tx_id": "TXN-003", "date": "02/10/2023", "product": "Monitor 24 inch", "price": "2000000", "qty": "1"}, # Format tanggal beda & qty string
    {"tx_id": "TXN-004", "date": "2023-10-02", "product": "HDMI Cable", "price": None, "qty": 5}, # Price kosong (corrupt data)
    {"tx_id": "TXN-005", "date": "2023-10-03", "product": "KEYBOARD MECHANICAL", "price": "500000", "qty": 1}
]

#1. Function & string methods

'''Fungsi tuk menghapus spasi di awal dan akhir dan menjadikkan title case'''
def clean_text(product_name):
    '''pastikan yg masuk ke fungsi ini adalah string (defensive programming)'''
    if not isinstance(product_name, str):
        return "Unkown" 
    return product_name.strip().title()


'''Fungsi tuk Standardisasi format tanggal sesuai standar ISO Database -> (YYYY-MM-DD)
output adalah String Object'''
from datetime import datetime 

def standardize_date(date_str):
    '''parsing objek String jadi Datetime'''
    try:
        #mencoba parsing format YYYY-MM-DD
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:                  
        try: 
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except:
            return None

    
#2. Main ETL Process
clean_data = [] #list kosong tuk menampung data bersih
total_revenue = 0

print("---Memulai Proses ETL---")

#Control Flow: Loop
for row in raw_data:
    # A. Data Extraction & Validation (Variables & If-Else)
    price = row.get("price")
    qty = row.get("qty")

    # Filter: Buang data jika price kosong (Data Quality Check)
    if price is None:
        print(f"Skipping corrupt data: {row["tx_id"]}")
        continue #lanjut ke data berikutnya (kalo gk corrupt) / looping

    # B. Transformation (Type Casting & Calculations)
    try:
        # Type Casting: String ke Float/Int
        price_float = float(price)
        qty_int = int(qty)

        #String Manipulation
        cleaned_product = clean_text(row["product"])

        #Date Handling
        cleaned_date = standardize_date(row["date"])

        if cleaned_date is None:
            print(f"Invalid date for {row["tx_id"]}")
            continue
            
        #Calculation
        total_sales = price_float * qty_int

        # C. Load to Structure (Dict Construction)
        transformed_row = {
            "transaction_id": row["tx_id"],
            "date": cleaned_date,
            "product_name": cleaned_product,
            "total_sales": total_sales
        }

        clean_data.append(transformed_row) 

        #agg
        total_revenue += total_sales

    except ValueError as e:
        print(f"Error processing row {row["tx_id"]}: {e}")

#4. Output 
print(f"\n--- Data bersih (ready for warehouse) ---")
for item in clean_data:
    print(item)

print(f"\n --- Total Revenue: {total_revenue:,.2f}")







