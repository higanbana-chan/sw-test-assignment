'''
3 : เขียนโปรแกรม
เขียนโปรแกรม 
1. input 1 value (max 3 digits) 
2. Put input into stack (215)
3. Pop and change to character 
    input 215 => exp output = สองร้อยสิบห้าบาทถ้วน
'''

def number_to_thai_text(number):
    # กำหนดค่าพื้นฐาน
    digits = ["ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
    units = ["", "สิบ", "ร้อย"]
    
    # แปลงตัวเลขเป็น list ของตัวอักษรเพื่อใส่ Stack
    # เช่น "215" -> ['2', '1', '5']
    stack = list(str(number))
    result = ""
    
    # วนลูปตามจำนวนหลัก (สูงสุด 3 หลัก)
    length = len(stack)
    for i in range(length):
        # Pop ตัวหน้าสุดออกมา (ใน Python ใช้ pop(0) เพื่อเลียนแบบการดึงหลักที่สำคัญที่สุดก่อน)
        digit = int(stack.pop(0))
        curr_pos = length - i - 1  # ตำแหน่งหลัก (2=ร้อย, 1=สิบ, 0=หน่วย)

        if digit != 0:
            # จัดการกรณีพิเศษของหลักสิบ (เอ็ด / ยี่ / สิบ)
            if curr_pos == 1 and digit == 1:
                result += "สิบ"
            elif curr_pos == 1 and digit == 2:
                result += "ยี่สิบ"
            # จัดการกรณีพิเศษของหลักหน่วย (เอ็ด)
            elif curr_pos == 0 and digit == 1 and length > 1:
                result += "เอ็ด"
            else:
                result += digits[digit] + units[curr_pos]
                
    return result + "บาทถ้วน"

# --- ส่วนการรับ Input และแสดงผล ---
if __name__ == "__main__":
    user_input = input("Enter 1-3 digit number: ")
    
    # Validation เบื้องต้นสำหรับ Testing
    if user_input.isdigit() and len(user_input) <= 3:
        output = number_to_thai_text(user_input)
        print(f"Input {user_input} => exp output = {output}")
    else:
        print("Error: Please enter 1-3 digits only.")