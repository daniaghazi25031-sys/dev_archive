import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow import keras
import plotly.express as px

# 1. إعدادات الصفحة
st.set_page_config(page_title="CREDO AI - Smart Logic", layout="wide")

# 2. بيانات تدريبية واقعية وشاملة
@st.cache_data
def load_comprehensive_data():
    np.random.seed(42)
    n_samples = 5000
    
    data = {
        'age': np.random.randint(22, 65, n_samples),
        'total_income': np.random.choice(np.arange(500000, 10000000, 250000), n_samples),
        'existing_loans_count': np.random.choice([0, 1, 2, 3], n_samples, p=[0.6, 0.2, 0.1, 0.1]),
        'monthly_obligations': np.random.randint(0, 1500000, n_samples), # أقساط خارجية
        'credit_score': np.random.uniform(0, 100, n_samples),
        'requested_amount': np.random.randint(1000000, 150000000, n_samples),
        'duration_months': np.random.randint(12, 120, n_samples),
        'collateral_val': np.random.randint(0, 200000000, n_samples),
        'job': np.random.choice([0, 1, 2, 3, 4], n_samples) # مشفرة للتدريب
    }
    
    df = pd.DataFrame(data)
    
    # منطق القبول المرن والواقعي
    targets = []
    for i in range(n_samples):
        # حساب الدخل المتاح بعد الخصومات
        disposable_income = df.at[i, 'total_income'] - df.at[i, 'monthly_obligations'] - (df.at[i, 'existing_loans_count'] * 100000)
        monthly_inst = df.at[i, 'requested_amount'] / df.at[i, 'duration_months']
        
        score = 0
        if monthly_inst < (disposable_income * 0.5): score += 4 # قدرة سداد جيدة
        if df.at[i, 'collateral_val'] > df.at[i, 'requested_amount']: score += 4 # ضمانات كافية جداً
        if df.at[i, 'credit_score'] > 50: score += 2 # سجل مقبول
        
        targets.append(1 if score >= 5 else 0) # مرونة في القبول
        
    df['target'] = targets
    return df

# 3. تدريب النظام
@st.cache_resource
def train_ai_engine():
    df = load_comprehensive_data()
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    
    rf = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)
    
    model = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X_train_sc, y_train, epochs=10, verbose=0)
    
    return rf, model, scaler

rf_model, dl_model, scaler = train_ai_engine()

# 4. الواجهة الاحترافية
st.markdown("<h1 style='text-align: center; color: #1A5276;'> LOAN SYSTEM — CREDO PRO</h1>", unsafe_allow_html=True)
st.divider()

c1, c2 = st.columns([1, 1.2])

with c1:
    st.subheader(" معلومات الطلب التفصيلية")
    
    with st.container(border=True):
        name = st.text_input("اسم العميل")
        age = st.number_input("العمر", 22, 65, 30)
        job = st.selectbox("القطاع الوظيفي", ['حكومي', 'قطاع خاص', 'عمل حر', 'صاحب عمل', 'بدون عمل'])
        location = st.radio("Residency", ["Urban", "Rural"], horizontal=True)
        job_map = {'حكومي':0, 'قطاع خاص':1, 'عمل حر':2, 'صاحب عمل':3, 'بدون عمل':4}

    with st.container(border=True):
        st.write("التحليل المالي المتقدم")
        total_inc = st.number_input("الراتب الكلي (دينار)", 250000, 20000000, 1000000)
        
        # حقل الالتزامات الجديدة
        st.info("الالتزامات الشهرية الحالية (أقساط سيارة، أجهزة، منزل...)")
        monthly_fixed_costs = st.number_input("مجموع الأقساط الخارجية", 0, 5000000, 0)
        
        existing_loans = st.number_input("عدد القروض البنكية الحالية", 0, 5, 0)
        credit_score = st.slider("درجة السجل الائتماني", 0, 100, 70)

    with st.container(border=True):
        req_amt = st.number_input("مبلغ القرض المطلوب", 1000000, 500000000, 10000000)
        years = st.slider("مدة القرض (سنوات)", 1, 15, 3)

    with st.expander("🛡️ الضمانات البنكية"):
        collateral_type = st.multiselect("نوع الضمان", ["عقار", "سيارة", "أرض", "كفالة شخصية"])
        collateral_val = st.number_input("القيمة التقديرية الكلية للضمانات", 0, 1000000000, 0)

with c2:
    st.subheader(" فحص الجدارة الائتمانية")
    
    if st.button("تحليل الطلب وإصدار القرار", type="primary", use_container_width=True):
        # الحسابات المالية الصافية
        net_income = total_inc - monthly_fixed_costs
        # افتراض أن كل قرض قديم يستقطع 15% من الراتب
        loan_deductions = existing_loans * (total_inc * 0.1)
        final_disposable_income = net_income - loan_deductions
        
        monthly_payment = req_amt / (years * 12)
        dti = monthly_payment / final_disposable_income if final_disposable_income > 0 else 999
        
        # عرض البيانات المالية الصافية
        st.metric("الراتب الصافي المتاح للسداد", f"{final_disposable_income:,.0f} د.ع")
        st.metric("القسط الشهري المتوقع", f"{monthly_payment:,.0f} د.ع")

        # تحضير البيانات للـ AI
        input_data = np.array([[age, total_inc, existing_loans, monthly_fixed_costs, credit_score, req_amt, years*12, collateral_val, job_map[job]]])
        
        # التنبؤ
        rf_p = rf_model.predict_proba(input_data)[0][1]
        dl_p = dl_model.predict(scaler.transform(input_data), verbose=0)[0][0]
        final_score = (rf_p * 0.5) + (dl_p * 0.5)

        st.divider()
        
        # منطق القرار مع ذكر الأسباب
        reasons = []
        if dti > 0.6: reasons.append("القسط المطلوب مرتفع جداً بالنسبة لصافي راتبك.")
        if credit_score < 25: reasons.append("سجلك الائتماني منخفض جدا(اقل من الحد الادنى للمخاطره)")
        #edit
        elif credit_score <40:
             reasons.append("سجلك الائتماني السابق ضعيف ويحتاج تحسين.")
        if req_amt > 20000000 and collateral_val < req_amt: reasons.append("المبلغ كبير ويحتاج ضمانات (عقار أو أرض) تغطي القيمة.")
        if existing_loans >= 3: reasons.append("لديك عدد كبير من القروض النشطة حالياً.")

        if credit_score>=25 and dti<= 0.6 and (final_score > 0.4 or (collateral_val > req_amt )): # مرونة: إذا الضمانات قوية جداً يوافق
            st.balloons()
            st.success(f"✅ تم قبول الطلب بنسبة ثقة {final_score:.1%}")
            if collateral_val > req_amt:
                st.caption("ملاحظة: تم القبول بشكل أساسي لقوة الضمانات المقدمة.")
        else:
            st.error(f"❌ الطلب مرفوض (درجة المخاطرة: {1-final_score:.1%})")
            st.write("**أسباب الرفض المنطقية:**")
            for r in reasons:
                st.write(f"- {r}")
            if not reasons:
                st.write("- تضارب في بيانات الدخل مع الالتزامات الشهرية.")

    st.divider()
    # إحصائية بسيطة
    st.write("####  توزيع القروض المقبولة حسب الدخل")
    chart_data = load_comprehensive_data().sample(200)
    fig = px.bar(chart_data, x="total_income", y="requested_amount", color="target", 
                 labels={"target":"حالة القبول", "total_income":"الدخل"},
                 color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)
# 3. تدريب النظام مع طباعة النتائج في الـ Terminal
@st.cache_resource
def train_ai_engine():
    df = load_comprehensive_data()
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # تدريب Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
    
    # حساب الدقة لاختبار النموذج
    from sklearn.metrics import accuracy_score, classification_report
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # --- طباعة النتائج في الـ Terminal ---
    print("\n" + "="*50)
    print("🚀 CREDO AI SYSTEM - PERFORMANCE REPORT")
    print("="*50)
    print(f"✅ Model Accuracy: {acc:.2%}")
    print("-" * 30)
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    print("-" * 30)
    print("💡 Feature Importance (Most Influential Factors):")
    
    importances = rf.feature_importances_
    for name, importance in zip(X.columns, importances):
        print(f" - {name:20}: {importance:.4f}")
    print("="*50 + "\n")
    # ---------------------------------------

    # تدريب Deep Learning
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    
    model = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X_train_sc, y_train, epochs=10, verbose=0)
    
    return rf, model, scaler

rf_model, dl_model, scaler = train_ai_engine()
# ==========================================
# terminal report: big data analysis
# ==========================================
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 1. prepare testing data
test_df = load_comprehensive_data()
x_test_raw = test_df.drop('target', axis=1)
y_true = test_df['target']

# 2. get predictions from both models
# random forest
rf_preds = rf_model.predict(x_test_raw)
rf_acc = accuracy_score(y_true, rf_preds)

# deep learning
x_test_scaled = scaler.transform(x_test_raw)
dl_probs = dl_model.predict(x_test_scaled, verbose=0)
dl_preds = (dl_probs > 0.5).astype(int)
dl_acc = accuracy_score(y_true, dl_preds)

# 3. printing the results to terminal
print("\n" + "📊" + " --- logicgate: credio pro analysis ---")
print(f"data source: synthetic dataset | samples: {len(test_df)}")
print("-" * 60)
print(f"{'method':<25} | {'accuracy score':<15}")
print("-" * 60)
print(f"{'random forest':<25} | {rf_acc:.2%}")
print(f"{'deep learning (nn)':<25} | {dl_acc:.2%}")
print("-" * 60)

# comparison logic
best_performer = "random forest" if rf_acc > dl_acc else "deep learning"
print(f"💡 final verdict: the best performing model is {best_performer}")
print("--- report generated successfully ---\n")
# ==========================================
# selection logic: filtering top 5% from 200
# ==========================================

# 1. sampling 200 candidates from the dataset
n_candidates = 200
selection_df = load_comprehensive_data().sample(n_candidates).reset_index(drop=True)
x_val = selection_df.drop('target', axis=1)

# 2. predicting probabilities (scoring)
# getting scores from random forest
rf_probs = rf_model.predict_proba(x_val)[:, 1]

# getting scores from deep learning (neural network)
x_val_scaled = scaler.transform(x_val)
dl_probs = dl_model.predict(x_val_scaled, verbose=0).flatten()

# 3. appending scores to the dataframe
selection_df['rf_score'] = rf_probs
selection_df['dl_score'] = dl_probs

# 4. selecting the top 5% (top 10 candidates)
top_count = int(n_candidates * 0.05)
best_rf = selection_df.nlargest(top_count, 'rf_score')
best_dl = selection_df.nlargest(top_count, 'dl_score')

# 5. terminal output formatting
print("\n" + "🎯" + " --- ai selection report: the elite 5% ---")
print(f"total candidates analyzed: {n_candidates} | selected: {top_count}")

print("\n--- [top 10 picks by random forest] ---")
for i, (idx, row) in enumerate(best_rf.iterrows()):
    print(f"rank {i+1:2} | prob: {row['rf_score']:.2%} | income: {row['total_income']:,} idc")

print("\n--- [top 10 picks by deep learning] ---")
for i, (idx, row) in enumerate(best_dl.iterrows()):
    print(f"rank {i+1:2} | prob: {row['dl_score']:.2%} | income: {row['total_income']:,} idc")

print("\n" + "✅" + " selection process finished successfully.")