import tkinter as tk
from tkinter import messagebox

# ----------------------------------------------------
# A. BUSINESS LOGIC CLASS (Logic เดิมของคุณ)
# ... (ส่วนนี้ไม่มีการเปลี่ยนแปลง)
# ----------------------------------------------------
class NumberToCurrency:
# ... (โค้ดเดิม)
    def __init__(self):
        # Dictionary สำหรับแปลงตัวเลขเป็นคำศัพท์ (ภาษาอังกฤษ)
        self.units = {0: "", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                      6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
        
        self.teens = {10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
                      15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen", 19: "Nineteen"}
        
        self.tens = {2: "Twenty", 3: "Thirty", 4: "Forty", 5: "Fifty",
                     6: "Sixty", 7: "Seventy", 8: "Eighty", 9: "Ninety"}

    def convert(self, number_str):
        # ... (โค้ดเดิม)
        if not number_str.isdigit():
            return "Error: Input must be numeric."
        if len(number_str) > 3:
            return "Error: Max 3 digits allowed."
        
        try:
            num_val = int(number_str)
        except ValueError:
            return "Error: Invalid number format."
            
        if num_val == 0:
            return "Zero Baht Only"

        temp_str = str(num_val)

        stack = []
        for digit in reversed(temp_str):
            stack.append(int(digit))
        
        result_parts = []
        
        while stack:
            place_value = len(stack) 
            digit = stack.pop() 

            if place_value == 3:
                if digit > 0:
                    result_parts.append(self.units[digit] + " Hundred")

            elif place_value == 2:
                if digit == 1:
                    next_digit = stack.pop() 
                    val = 10 + next_digit
                    result_parts.append(self.teens[val])
                elif digit > 1:
                    result_parts.append(self.tens[digit])
            
            elif place_value == 1:
                if digit > 0:
                    result_parts.append(self.units[digit])

        return " ".join(result_parts) + " Baht"

# ----------------------------------------------------
# B. UI (TKINTER) APPLICATION CLASS
# ----------------------------------------------------
class CurrencyConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Number to Currency Converter (Max 3 Digits)")

        self.converter = NumberToCurrency()

        # เราจะเพิ่ม Background สีดำให้กับ Frame เพื่อให้ตัวอักษรสีขาวดูโดดเด่นขึ้น
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        # 1. Input Field
        self.label_input = tk.Label(self.main_frame, text="Enter Number (0-999):", font=('Arial', 12))
        self.label_input.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.input_var = tk.StringVar()
        self.entry_input = tk.Entry(self.main_frame, textvariable=self.input_var, font=('Arial', 12), width=15)
        self.entry_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.entry_input.bind('<Return>', lambda event: self.convert_number())

        # 2. Convert Button
        self.button_convert = tk.Button(self.main_frame, text="Convert", command=self.convert_number, font=('Arial', 12, 'bold'))
        self.button_convert.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 3. Output Field
        # เพิ่ม Frame เพื่อควบคุมสีพื้นหลังของส่วน Output
        self.output_frame = tk.Frame(self.main_frame, bg="black")
        self.output_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        self.main_frame.grid_columnconfigure(1, weight=1) # ให้คอลัมน์ Input ขยาย
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1) # ให้ Label ใน Frame ขยาย

        self.output_var = tk.StringVar()
        
        # ******** ส่วนที่ถูกแก้ไข *********
        self.label_output = tk.Label(
            self.output_frame, 
            textvariable=self.output_var, 
            font=('Arial', 14, 'bold'), # ตัวหนา (Bold)
            fg="white",                 # สีขาว (White)
            bg="black",                 # สีพื้นหลัง (เพื่อให้เห็นตัวอักษรสีขาวชัดเจน)
            wraplength=400, 
            justify=tk.CENTER,          # จัดข้อความภายใน Label ให้อยู่กึ่งกลาง
            anchor="center"             # จัดตำแหน่งของ Label ให้อยู่กึ่งกลางใน Frame
        )
        self.label_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 
        # *********************************

    def convert_number(self):
        number_str = self.input_var.get().strip()
        
        if not number_str:
            self.output_var.set("Please enter a number.")
            return

        result = self.converter.convert(number_str)

        if result.startswith("Error"):
            messagebox.showerror("Input Error", result)
            self.output_var.set("")
        else:
            self.output_var.set(result)

# ----------------------------------------------------
# C. RUN APPLICATION
# ----------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()