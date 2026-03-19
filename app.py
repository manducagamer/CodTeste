import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Calculadora de IMC",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
        :root {
            --primary-color: #00d4ff;
            --secondary-color: #0a0e27;
            --text-color: #e0e0e0;
            --success-color: #44ff44;
            --error-color: #ff4444;
            --warning-color: #ffaa00;
        }
        
        body {
            background-color: #0a0e27;
            color: #e0e0e0;
        }
        
        .main {
            background-color: #0a0e27;
        }
        
        .stMetric {
            background-color: #1a1f3a;
            border-radius: 10px;
            padding: 20px;
        }
        
        h1, h2, h3 {
            color: #00d4ff;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>⚕️ CALCULADORA DE IMC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Calcule seu Índice de Massa Corporal e receba uma avaliação completa</p>", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
    st.session_state.results = {}

# Input section
st.markdown("### 📋 DADOS PESSOAIS")

col1, col2 = st.columns(2)

with col1:
    weight_kg = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=0.0)
    height = st.number_input("Altura (m)", min_value=0.0, step=0.01, value=0.0, format="%.2f")

with col2:
    weight_g = st.number_input("Gramas (g)", min_value=0, step=1, value=0)
    age = st.number_input("Idade", min_value=0, step=1, value=0)

sex = st.radio("Sexo", ["Masculino", "Feminino"], horizontal=True)

# Calculate button
if st.button("🔢 CALCULAR", use_container_width=True, type="primary"):
    if weight_kg <= 0 or height <= 0 or age <= 0:
        st.error("❌ Por favor, preencha todos os campos com valores válidos!")
    else:
        st.session_state.calculated = True
        
        # Calculate total weight
        total_weight = weight_kg + (weight_g / 1000)
        
        # Calculate BMI
        imc = total_weight / (height * height)
        
        # Calculate ideal weight
        if sex == "Masculino":
            peso_ideal = (72.7 * height) - 58
        else:  # Feminino
            peso_ideal = (62.1 * height) - 44.7
        
        # Calculate difference
        difference = total_weight - peso_ideal
        
        # Determine classification
        if imc < 18.5:
            classification = "Abaixo do Peso"
            status_color = "🔴"
        elif imc < 25:
            classification = "Peso Normal"
            status_color = "🟢"
        elif imc < 30:
            classification = "Sobrepeso"
            status_color = "🟡"
        elif imc < 35:
            classification = "Obesidade Grau I"
            status_color = "🟠"
        elif imc < 40:
            classification = "Obesidade Grau II"
            status_color = "🟠"
        else:
            classification = "Obesidade Grau III"
            status_color = "🔴"
        
        # Store results
        st.session_state.results = {
            'total_weight': total_weight,
            'imc': imc,
            'peso_ideal': peso_ideal,
            'difference': difference,
            'classification': classification,
            'status_color': status_color
        }

# Results section
if st.session_state.calculated:
    st.markdown("---")
    st.markdown("### 📊 RESULTADOS")
    
    results = st.session_state.results
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Peso Total", f"{results['total_weight']:.2f} kg")
    
    with col2:
        st.metric("IMC", f"{results['imc']:.2f}")
    
    with col3:
        st.metric("Peso Ideal", f"{results['peso_ideal']:.2f} kg")
    
    with col4:
        diff_text = f"+{results['difference']:.2f}" if results['difference'] >= 0 else f"{results['difference']:.2f}"
        st.metric("Diferença", f"{diff_text} kg")
    
    # Status
    st.markdown("---")
    status_box = f"""
    <div style='
        background: linear-gradient(135deg, #1a1f3a 0%, #2a2f4a 100%);
        border-left: 5px solid #00d4ff;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    '>
        <h2 style='color: #00d4ff; margin: 0;'>Status de Saúde</h2>
        <h1 style='color: #00d4ff; margin: 10px 0;'>{results['status_color']} {results['classification']}</h1>
        <p style='color: #888; margin: 0;'>Baseado no seu IMC</p>
    </div>
    """
    st.markdown(status_box, unsafe_allow_html=True)
    
    # BMI Chart
    st.markdown("---")
    st.markdown("### 📈 Faixa de IMC")
    
    bmi_ranges = pd.DataFrame({
        'Classificação': ['Abaixo do Peso', 'Peso Normal', 'Sobrepeso', 'Obesidade I', 'Obesidade II', 'Obesidade III'],
        'IMC Min': [0, 18.5, 25, 30, 35, 40],
        'IMC Max': [18.5, 25, 30, 35, 40, 100],
        'Status': ['🔴', '🟢', '🟡', '🟠', '🟠', '🔴']
    })
    
    st.table(bmi_ranges)
    
    # Health recommendations
    st.markdown("---")
    st.markdown("### 💡 Recomendações")
    
    if results['imc'] < 18.5:
        st.info("Você está abaixo do peso ideal. Consulte um médico ou nutricionista para aumentar sua ingestão calórica de forma saudável.")
    elif results['imc'] < 25:
        st.success("Parabéns! Seu peso está na faixa considerada saudável. Continue mantendo hábitos saudáveis!")
    elif results['imc'] < 30:
        st.warning("Você está com sobrepeso. Considere aumentar atividades físicas e revisar sua alimentação.")
    else:
        st.error("Você está acima do peso recomendado. Procure um profissional de saúde para orientações sobre perda de peso.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        <p>© 2026 - Calculadora de IMC Interativa | Feito com ❤️ usando Streamlit</p>
    </div>
""", unsafe_allow_html=True)
