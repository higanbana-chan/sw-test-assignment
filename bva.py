import matplotlib.pyplot as plt
import matplotlib.patches as patches

def get_bva_values(min_val, max_val):
    """สร้างค่า BVA 5 ค่าพื้นฐาน: min, min+1, mid, max-1, max"""
    mid = (min_val + max_val) // 2
    return sorted(list(set([min_val, min_val + 1, mid, max_val - 1, max_val])))

def get_robustness_values(min_val, max_val):
    """สร้างค่า Robustness 7 ค่า: เพิ่ม min-1 และ max+1"""
    base = get_bva_values(min_val, max_val)
    return sorted(list(set(base + [min_val - 1, max_val + 1])))

def main():
    print("--- Test Case Generator (BVA Family) ---")
    
    # 1. Input Section
    try:
        min_x = int(input("Enter Min X: "))
        max_x = int(input("Enter Max X: "))
        min_y = int(input("Enter Min Y: "))
        max_y = int(input("Enter Max Y: "))
        
        print("\nSelect Method:")
        print("1. BVA (Boundary Value Analysis)")
        print("2. Robustness")
        print("3. Worst Case")
        print("4. Worst Case Robustness")
        method = int(input("Select choice (1-4): "))
    except ValueError:
        print("Error: Please enter integer numbers only.")
        return

    # 2. Calculate Mid Values (Nominal)
    mid_x = (min_x + max_x) // 2
    mid_y = (min_y + max_y) // 2

    # 3. Determine Values of Interest based on Method
    # ถ้าเลือก method ที่เป็น Robustness จะใช้เซ็ตค่าที่มี min-1, max+1
    use_robustness = (method == 2 or method == 4)
    
    if use_robustness:
        x_vals = get_robustness_values(min_x, max_x)
        y_vals = get_robustness_values(min_y, max_y)
    else: # BVA or Worst Case
        x_vals = get_bva_values(min_x, max_x)
        y_vals = get_bva_values(min_y, max_y)

    # 4. Generate Test Cases (Pairing Strategy)
    test_cases = [] # List เก็บ tuple (x, y)

    is_worst_case = (method == 3 or method == 4)

    if is_worst_case:
        # Worst Case: จับคู่ทุกตัวกับทุกตัว (Cartesian Product)
        for x in x_vals:
            for y in y_vals:
                test_cases.append((x, y))
    else:
        # Standard BVA/Robustness: Single Fault Assumption
        # ยึดค่าหนึ่งเป็น Nominal แล้วเปลี่ยนอีกค่าหนึ่ง
        
        # กรณี Base Case (Nominal, Nominal)
        test_cases.append((mid_x, mid_y))
        
        # Vary X, Hold Y at Nominal
        for x in x_vals:
            if x != mid_x: # ไม่เอาค่าซ้ำ
                test_cases.append((x, mid_y))
                
        # Vary Y, Hold X at Nominal
        for y in y_vals:
            if y != mid_y: # ไม่เอาค่าซ้ำ
                test_cases.append((mid_x, y))

    # 5. Calculate Z and Display Table
    print("\n" + "="*40)
    print(f"{'No.':<5} {'X':<10} {'Y':<10} {'Z (Expected)':<15}")
    print("="*40)
    
    for i, (x, y) in enumerate(test_cases, 1):
        z = x * y
        print(f"{i:<5} {x:<10} {y:<10} {z:<15}")

    print("="*40)
    print(f"Total Test Cases: {len(test_cases)}")

    # 6. Plot Graph
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # วาดกรอบ Valid Input Domain (พื้นที่ที่ถูกต้อง)
    width = max_x - min_x
    height = max_y - min_y
    rect = patches.Rectangle((min_x, min_y), width, height, 
                             linewidth=2, edgecolor='g', facecolor='none', label='Valid Domain')
    ax.add_patch(rect)

    # แยก X, Y เพื่อ plot จุด
    xs = [tc[0] for tc in test_cases]
    ys = [tc[1] for tc in test_cases]

    # Plot จุด Test Case
    # สีแดง = จุดที่อยู่นอกขอบเขต (Invalid), สีน้ำเงิน = จุดปกติ
    colors = []
    for x, y in test_cases:
        if (min_x <= x <= max_x) and (min_y <= y <= max_y):
            colors.append('blue')
        else:
            colors.append('red')

    ax.scatter(xs, ys, c=colors, marker='o', s=50, label='Test Cases')
    
    # ตั้งค่ากราฟ
    plt.title(f"Test Cases Distribution (Method: {method})")
    plt.xlabel("Input X")
    plt.ylabel("Input Y")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # ปรับขอบเขตการแสดงผลกราฟให้กว้างกว่าจุดนิดหน่อย
    buffer_x = (max_x - min_x) * 0.2 if (max_x - min_x) > 0 else 5
    buffer_y = (max_y - min_y) * 0.2 if (max_y - min_y) > 0 else 5
    plt.xlim(min(xs) - buffer_x, max(xs) + buffer_x)
    plt.ylim(min(ys) - buffer_y, max(ys) + buffer_y)
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()