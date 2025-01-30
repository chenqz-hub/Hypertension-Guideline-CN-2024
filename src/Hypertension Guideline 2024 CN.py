import tkinter as tk
from tkinter import ttk, Toplevel

# 初始化风险因素字典
risk_factors = {
    "心血管危险因素": [
        "高血压(1~3级)",
        "年龄>55岁(男);>65岁(女)",
        "吸烟或被动吸烟",
        "糖耐量受损(2h血糖7.8~11.0mmol/L)\n和/或空腹血糖受损(6.1~6.9mmol/L)",
        "血脂异常\n(TC≥5.2mmol/L或LDL>3.4mmol/L或HDL<1.0mmol/L)",
        "早发心血管病家族史\n（一级亲属发病年龄<50岁)",
        "腹型肥胖(腰围:男≥90cm/女≥85cm)\n或肥胖(BMI≥28kg/m²)",        
        "高同型半胱氨酸\n(≥10μmol/L)",
        "高尿酸血症（血尿酸:男性≥420μmol/L，女性≥360μmol/L）",
        "心率增快（静息心率>80次/min）"
    ],
    "靶器官损害": [
        "左心室肥厚：\n心电图:Sokolow-Lyon电压>3.8mV或Cornell乘积>224mV·ms\n或超声心动图:LVMI≥109g/m²(男),≥105/m²(女)",
        "颈动脉超声IMT≥0.9mm或动脉粥样硬化斑块",
        "颈股PWV≥10m/s或肱踝PWV≥18m/s",
        "ABI<0.9",
        "eGFR 30~59ml/(min·1.73m²)\n或血肌酐轻度升高（男性115~133μmol/L;女性107~124μmol/L",
        "微量白蛋白尿：\n白蛋白/肌酐比值≥30mg/g或白蛋白排泌率30~300mg/24h"
    ],
    "伴随临床疾病": [
        "脑血管病：\n脑出血,缺血性脑卒中,TIA",
        "心脏疾病：\n心梗,心绞痛,冠状动脉血运重建,慢性心力衰竭,房颤",
        "肾脏疾病：\n糖尿病肾病，\n肾功能受损,包括：eGFR<30ml/(min·1.73m²)\n或肌酐≥133μmol/L(男);≥124μmol/L(女),或尿蛋白≥300mg/24h)",
        "外周动脉疾病",
        "视网膜病变：\n眼底出血或渗出，视乳头水肿",
        "糖尿病"
    ],
    "其他情况": [
        "CKD3期(eGFR 30~59ml/(min·1.73m²))",
        "CKD≥4期(eGFR<30ml/(min·1.73m²))",
        "无并发症的糖尿病",
        "有并发症的糖尿病"
    ]
}

# 全局变量
bp_level = ""
risk_level = ""
age = 0  # 用于存储输入的年龄

def calculate_risk():
    global bp_level
    try:
        sbp = int(sbp_entry.get()) if sbp_entry.get() else 0
        dbp = int(dbp_entry.get()) if dbp_entry.get() else 0
        age = int(age_entry.get()) if age_entry.get() else 0
    except ValueError:
        bp_result_text.set("错误：血压值和年龄必须为整数")
        return

    # 确定血压分级
    if sbp >= 180 or dbp >= 110:
        bp_level = "高血压3级"
    elif sbp >= 160 or dbp >= 100:
        bp_level = "高血压2级"
    elif sbp >= 140 or dbp >= 90:
        bp_level = "高血压1级"
    elif 139 >= sbp >= 130 or 89 >= dbp >= 80:
        bp_level = "正常高值血压"
    else:
        bp_level = "正常血压"

    bp_result_text.set(bp_level)  # 只设置分级结果
    show_risk_factors()  # 显示风险因素选择部分

def show_risk_factors():
    check_frame.pack(padx=10, pady=5, fill="both", expand=True)

def calculate_final_risk():
    global bp_level, risk_level
    # 获取勾选状态
    selected_clinical = [risk_factors["伴随临床疾病"][i] for i, var in enumerate(clinical_vars) if var.get() == 1]
    selected_other = [risk_factors["其他情况"][i] for i, var in enumerate(other_vars) if var.get() == 1]
    has_clinical_disease = any(selected_clinical)
    has_target_organ = any(var.get() for var in target_vars)
    total_risk = sum(var.get() for var in risk_vars)
    has_ckd3_or_no_complications_diabetes = any(item in selected_other for item in ["CKD3期", "无并发症的糖尿病"])

    # 分层逻辑
    if has_clinical_disease or (("CKD≥4期" in selected_other or "有并发症的糖尿病" in selected_other) and has_target_organ):
        if bp_level == "正常高值血压":
            risk_level = "高-很高危"
        else:
            risk_level = "很高危"
    elif has_target_organ or total_risk >= 3 or (("CKD3期" in selected_other or "无并发症的糖尿病" in selected_other) and has_target_organ):
        if bp_level == "正常高值血压":
            risk_level = "中-高危"
        else:
            risk_level = "高危" if bp_level in ["高血压1级", "高血压2级"] else "很高危"
    elif 1 <= total_risk <= 2:
        if bp_level == "正常高值血压":
            risk_level = "低危"
        elif bp_level == "高血压2级":
            risk_level = "中/高危"
        else:
            risk_level = "很高危" if bp_level == "高血压3级" else "中危"
    elif total_risk == 0:
        if bp_level == "高血压2级":
            risk_level = "中危"
        elif bp_level == "高血压3级":
            risk_level = "高危"
        else:
            risk_level = "低危"
    else:
        risk_level = "低危"

    risk_result_text.set(risk_level)
    show_treatment_button()  # 显示降压治疗策略按钮

def show_treatment_button():
    # 显示降压治疗策略按钮，使用pack()并确保占据整个宽度
    treatment_button.pack(pady=5, fill="x", expand=True)

def show_treatment_strategy():
    sbp = int(sbp_entry.get())
    dbp = int(dbp_entry.get())
    bp_grade = bp_result_text.get()  # 直接获取文本
    risk = risk_result_text.get()
    age = int(age_entry.get()) if age_entry.get() else 0  # 获取年龄
    analysis = f"收缩压: {sbp} mmHg\n舒张压: {dbp} mmHg\n血压分级: {bp_grade}\n心血管风险分层: {risk}\n\n降压治疗策略：\n"
    
    # 根据血压水平和心血管风险进行治疗策略判断
    if sbp >= 160 or dbp >= 100:
        analysis += "建议立即启动降压药物治疗(Ⅰ,A)。"
    elif 140 <= sbp <= 159 or 90 <= dbp <= 99:
        if risk_level in ["高危", "很高危"]:
            analysis += "建议立即启动降压药物治疗(Ⅰ,A)。"
        else:
            analysis += "建议改善生活方式4~12周, 如血压仍不达标, 应尽早启动降压药物治疗(Ⅰ,C)。"
    elif 130 <= sbp <= 139 or 85 <= dbp <= 89:
        if risk_level in ["高危", "很高危"]:
            analysis += "建议立即启动降压药物治疗(Ⅰ,B)。"
        else:
            analysis += "目前没有证据显示可以从降压药物治疗中获益, 此类人群应持续进行生活方式干预(Ⅰ,C)。"
    else:
        analysis += "血压在正常范围，请继续保持健康的生活方式。"
    
    # 添加降压目标逻辑，考虑年龄
    if age >= 80:
        target = "<150/90 mmHg，如可耐受<140/90 mmHg"  # 对于80岁及以上的高龄患者
    elif age >= 65:
        target = "<140/90 mmHg"  # 对于65岁及以上的老年人
    elif risk_level in ["高危", "很高危"] or any(var.get() == 1 for var in clinical_vars):  # 高危/很高危或伴随临床疾病
        target = "<130/80 mmHg"  # 高危/很高危或伴随临床疾病
    else:
        target = "<140/90 mmHg"  # 其他患者

    analysis += f"\n\n降压治疗目标：{target}"

    # 创建自定义弹窗
    top = Toplevel(root)  # 创建新的顶层窗口
    top.title("降压治疗策略")

    # 设置弹窗的大小
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()  # 获取屏幕宽度
    screen_height = root.winfo_screenheight()  # 获取屏幕高度
    position_top = int(screen_height / 2 - window_height / 2)  # 设置垂直位置
    position_right = int(screen_width / 2 - window_width / 2)  # 设置水平位置

    # 调整弹窗位置并设置大小
    top.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

    # 恢复弹窗背景为默认颜色
    top.config(bg="white")  # 设置弹窗背景为默认（白色）

    # 创建标签并显示分析结果，使用wraplength自动换行
    result_label = ttk.Label(top, text=analysis, justify=tk.LEFT, font=('Times New Roman', 10), background="white", wraplength=window_width-40)
    result_label.pack(padx=20, pady=20)

    # 确认按钮，关闭弹窗
    ttk.Button(top, text="确认", command=top.destroy).pack(pady=10)

# 创建主窗口
root = tk.Tk()
root.title("高血压心血管风险评估系统（中国高血压防治指南2024）")
root.geometry("600x700")  # 设置为更窄的窗口

# 血压输入部分
bp_frame = ttk.LabelFrame(root, text="血压测量（mmHg）")
bp_frame.pack(padx=10, pady=5, fill="x")

ttk.Label(bp_frame, text="收缩压：").grid(row=0, column=0, padx=5, pady=5)
sbp_entry = ttk.Entry(bp_frame)
sbp_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(bp_frame, text="舒张压：").grid(row=0, column=2, padx=5, pady=5)
dbp_entry = ttk.Entry(bp_frame)
dbp_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(bp_frame, text="年龄：").grid(row=1, column=0, padx=5, pady=5)
age_entry = ttk.Entry(bp_frame)
age_entry.grid(row=1, column=1, padx=5, pady=5)

# 结果输出部分
result_frame = ttk.Frame(root)
result_frame.pack(pady=10, fill="x")

ttk.Button(result_frame, text="计算血压分级", command=calculate_risk).pack(pady=5, fill="x")
bp_result_text = tk.StringVar()
ttk.Label(result_frame, textvariable=bp_result_text, font=('Arial', 12, 'bold')).pack(pady=5)

# 风险因素选择部分（带滚动条）
check_frame = ttk.LabelFrame(root, text="风险因素选择")
# 初始时不显示风险因素选择部分
check_frame.pack_forget()

canvas = tk.Canvas(check_frame)
scrollbar = ttk.Scrollbar(check_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")
check_frame.grid_rowconfigure(0, weight=1)
check_frame.grid_columnconfigure(0, weight=1)

# 支持鼠标滚轮滚动
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)

# 动态生成复选框
risk_vars = []
target_vars = []
clinical_vars = []
other_vars = []

for i, (category, factors) in enumerate(risk_factors.items()):
    group = ttk.LabelFrame(scrollable_frame, text=category)
    group.grid(row=i, column=0, padx=5, pady=5, sticky="w")
    
    var_list = risk_vars if category == "心血管危险因素" else target_vars if category == "靶器官损害" else clinical_vars if category == "伴随临床疾病" else other_vars
    
    for j, factor in enumerate(factors):
        var = tk.IntVar()
        cb = ttk.Checkbutton(group, text=factor, variable=var)
        cb.grid(row=j, column=0, sticky="w")
        var_list.append(var)

# 计算风险按钮放在最后
ttk.Button(scrollable_frame, text="计算心血管风险", command=calculate_final_risk).grid(row=len(risk_factors), column=0, pady=5, sticky="ew")
risk_result_text = tk.StringVar()
ttk.Label(scrollable_frame, textvariable=risk_result_text, font=('Arial', 12, 'bold')).grid(row=len(risk_factors) + 1, column=0, pady=5)

# 降压治疗策略按钮
treatment_button = ttk.Button(root, text="降压治疗策略", command=show_treatment_strategy)
# 初始时不显示按钮
treatment_button.pack_forget()

root.mainloop()