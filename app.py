import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

st.set_page_config(page_title="Propeller AI", page_icon="🚢", layout="centered")

st.title("🚢 تحليل الرفاص بالذكاء الاصطناعي")
st.write("مشروع هندسة بحرية - AI + 3D")

# AI Model
X_train = np.array([[0,1],[10,1.5],[20,2],[30,2],[40,2.5],[50,3],[60,3],[80,3.5]])
y_train = np.array([98,92,85,75,65,50,40,20])
ai_model = LinearRegression().fit(X_train, y_train)

# الواجهة
damage = st.slider("نسبة الضرر %", 0, 100, 30)
diameter = st.slider("قطر الرفاص بالمتر", 0.5, 10.0, 2.5, 0.1)

if st.button("تحليل + عرض 3D", type="primary", use_container_width=True):
    efficiency = ai_model.predict([[damage, diameter]])[0]
    efficiency = max(0, min(100, efficiency))

    if damage < 20: status, color = "آمن ✅", "green"
    elif damage < 50: status, color = "مراقبة ⚠️", "orange"
    else: status, color = "خطر ❌", "red"

    col1, col2 = st.columns(2)
    col1.metric("الكفاءة المتوقعة", f"{efficiency:.1f}%")
    col2.metric("الحالة", status)

    # رسم 3D
    st.subheader("شكل الرفاص 3D")
    fig = go.Figure()

    # الجسم Hub
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                               marker=dict(size=10, color='gray'), name='Hub'))

    # 3 ريش ملونة حسب الخطر
    for i in range(3):
        angle = np.radians(i * 120)
        x = [0, diameter * 0.8 * np.cos(angle)]
        y = [0, diameter * 0.8 * np.sin(angle)]
        z = [0, 0]
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines',
                                   line=dict(color=color, width=15), name=f'Blade {i+1}'))

    fig.update_layout(scene=dict(xaxis_title='', yaxis_title='', zaxis_title=''),
                      margin=dict(l=0,r=0,b=0,t=0), height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.caption("م. إسراء - هندسة بحرية 2026")