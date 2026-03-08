'''
เขียนโปรแกรมสร้าง test case file โดย
A. รับ input Width (min, max)
B. รับ input High (min, max)
C. เลือก BVA or Worse case, Robustness, Worse case robustness 
Loop:
       D. Generate Test case and Calculate TriangleArea(T) = (W * H)/2
       E. Write (Test Case ID, W, H, T);
 End;
0. สร้าง API CalTriangleSpace (W, H) Return Area integer.
1. ออกแบบ log file 
2.0 Input Tester Name
       Write "Tehis test run by ", TesterName
2. Get date time => Write to log
3. Input Tester name => Write to log
4. loop read test case file until end of file 
     call CalTriangleSpave(W, H) return Area.
     Compare Area with expected result
     If (Area=expected result)
        then write test case id, w, h, "Pass"
        else write test case id, w, h, "Fail"
     count number of test
     count number of pass
     count number of fail
   End lop
5. Get date time
6. Write "End of test at :", date time
7. WRite "Number of test", number of test
8. Write "Nunber of pass", number of pass
9. WRite "Number of fail", number of fail
'''

import csv
import datetime
import os

# ==========================================
# 0. API Section
# ==========================================
def cal_triangle_space(w, h):
    """
    0. API CalTriangleSpace (W, H) Return Area integer.
    สูตร: (W * H) / 2 (ปัดเศษทิ้งเป็นจำนวนเต็มตามโจทย์)
    """
    return int((w * h) / 2)

# ==========================================
# Helper Functions for Test Case Generation
# ==========================================
def get_bva_values(min_val, max_val):
    mid = (min_val + max_val) // 2
    return sorted(list(set([min_val, min_val + 1, mid, max_val - 1, max_val])))

def get_robustness_values(min_val, max_val):
    base = get_bva_values(min_val, max_val)
    return sorted(list(set(base + [min_val - 1, max_val + 1])))

# ==========================================
# Part 1: Generate Test Case File (A - E)
# ==========================================
def generate_test_case_file():
    print("\n--- Part 1: Generate Test Case File ---")
    # A. รับ input Width (min, max)
    w_min = int(input("Enter Width Min: "))
    w_max = int(input("Enter Width Max: "))
    
    # B. รับ input High (min, max)
    h_min = int(input("Enter Height Min: "))
    h_max = int(input("Enter Height Max: "))
    
    # C. เลือก Method
    print("\nSelect Method:")
    print("1. BVA")
    print("2. Robustness")
    print("3. Worst Case")
    print("4. Worst Case Robustness")
    method = int(input("Select choice (1-4): "))

    mid_w = (w_min + w_max) // 2
    mid_h = (h_min + h_max) // 2

    use_robustness = (method == 2 or method == 4)
    if use_robustness:
        w_vals = get_robustness_values(w_min, w_max)
        h_vals = get_robustness_values(h_min, h_max)
    else:
        w_vals = get_bva_values(w_min, w_max)
        h_vals = get_bva_values(h_min, h_max)

    test_cases = []
    is_worst_case = (method == 3 or method == 4)

    if is_worst_case:
        for w in w_vals:
            for h in h_vals:
                test_cases.append((w, h))
    else:
        # Base Case
        test_cases.append((mid_w, mid_h))
        # Vary W
        for w in w_vals:
            if w != mid_w: test_cases.append((w, mid_h))
        # Vary H
        for h in h_vals:
            if h != mid_h: test_cases.append((mid_w, h))

    # D & E. Generate Test case and Calculate T, Write to File
    filename = "test_cases.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Test Case ID", "W", "H", "Expected_T"])
        
        for i, (w, h) in enumerate(test_cases, 1):
            tc_id = f"TC{str(i).zfill(3)}"
            expected_t = cal_triangle_space(w, h) # T = (W*H)/2 integer
            writer.writerow([tc_id, w, h, expected_t])
            
    print(f"\nSuccess: Generated {len(test_cases)} test cases into '{filename}'")

# ==========================================
# Part 2: Automated Test Execution & Logging
# ==========================================
def run_automated_test():
    filename = "test_cases.csv"
    if not os.path.exists(filename):
        print("\nError: test_cases.csv not found. Please run Generation first.")
        return

    print("\n--- Part 2: Run Automated Test ---")
    # 2.0 / 3. Input Tester Name
    tester_name = input("Input Tester Name: ")
    
    log_filename = "test_log.txt"
    
    # Variables for counting
    total_test = 0
    pass_count = 0
    fail_count = 0

    with open(log_filename, mode='w', encoding='utf-8') as log_file:
        # 1. ออกแบบ log file (Header)
        log_file.write("="*50 + "\n")
        log_file.write(" AUTOMATED TEST LOG REPORT\n")
        log_file.write("="*50 + "\n")
        
        # 2. Get date time => Write to log
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"Start test at : {start_time}\n")
        
        # 3. Write Tester name to log
        log_file.write(f"This test run by : {tester_name}\n")
        log_file.write("-" * 50 + "\n")
        log_file.write(f"{'TC ID':<8} | {'W':<5} | {'H':<5} | {'Expected':<10} | {'Actual':<10} | {'Status'}\n")
        log_file.write("-" * 50 + "\n")

        # 4. Loop read test case file
        with open(filename, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                tc_id = row["Test Case ID"]
                w = int(row["W"])
                h = int(row["H"])
                expected_t = int(row["Expected_T"])
                
                # Call API
                actual_area = cal_triangle_space(w, h)
                
                total_test += 1
                
                # Compare Area
                if actual_area == expected_t:
                    status = "Pass"
                    pass_count += 1
                else:
                    status = "Fail"
                    fail_count += 1
                    
                # Write TC result
                log_file.write(f"{tc_id:<8} | {w:<5} | {h:<5} | {expected_t:<10} | {actual_area:<10} | {status}\n")
                
        # 5. Get date time (End)
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write Summary
        log_file.write("-" * 50 + "\n")
        # 6. Write End of test
        log_file.write(f"End of test at : {end_time}\n")
        # 7, 8, 9. Write counts
        log_file.write(f"Number of test : {total_test}\n")
        log_file.write(f"Number of pass : {pass_count}\n")
        log_file.write(f"Number of fail : {fail_count}\n")
        log_file.write("="*50 + "\n")

    print(f"\nSuccess: Automated test completed. View results in '{log_filename}'")

# ==========================================
# Main Menu
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n=== Main Menu ===")
        print("1. Generate Test Cases File")
        print("2. Run Automated Test")
        print("0. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            generate_test_case_file()
        elif choice == '2':
            run_automated_test()
        elif choice == '0':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")