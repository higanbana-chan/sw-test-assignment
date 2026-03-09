import graphviz

def create_cfg():
    # สร้าง Directed Graph
    dot = graphviz.Digraph('CFG', comment='Control Flow Graph: Assignment 5')
    dot.attr(rankdir='TB', size='8,10') # จัดเรียงจากบนลงล่าง

    # กำหนด Nodes และรูปทรง (Shape)
    dot.node('1', '1. Start/Input', shape='ellipse', style='filled', fillcolor='lightblue')
    dot.node('2', '2. Valid?', shape='diamond', style='filled', fillcolor='lightyellow')
    dot.node('3', '3. Error/Return', shape='box', style='filled', fillcolor='lightcoral')
    dot.node('4', '4. Robustness?', shape='diamond', style='filled', fillcolor='lightyellow')
    dot.node('5', '5. Get Robustness', shape='box')
    dot.node('6', '6. Get BVA', shape='box')
    dot.node('7', '7. Worst Case?', shape='diamond', style='filled', fillcolor='lightyellow')
    dot.node('8', '8. Loop WC', shape='box')
    dot.node('9', '9. Loop Std', shape='box')
    dot.node('10', '10. Print/Plot', shape='box')
    dot.node('11', '11. End', shape='doublecircle', style='filled', fillcolor='lightblue')

    # กำหนด Edges (เชื่อมโยงเส้นทาง)
    dot.edge('1', '2')
    dot.edge('2', '3', label='No (Invalid Input)')
    dot.edge('2', '4', label='Yes (Valid Input)')
    dot.edge('3', '11')
    dot.edge('4', '5', label='Yes')
    dot.edge('4', '6', label='No')
    dot.edge('5', '7')
    dot.edge('6', '7')
    dot.edge('7', '8', label='Yes')
    dot.edge('7', '9', label='No')
    dot.edge('8', '10')
    dot.edge('9', '10')
    dot.edge('10', '11')

    # เซฟเป็นไฟล์ PDF และเปิดดูอัตโนมัติ
    dot.render('whitebox_cfg_output', view=True, format='png')
    print("Graph generated successfully as 'whitebox_cfg_output.png'")

if __name__ == '__main__':
    create_cfg()