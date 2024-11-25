import streamlit as st
import datetime

 #conectando no css
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


usu_reserv={}

if "usu_reserv" not in st.session_state:
    st.session_state.usu_reserv = {"nome":None,"email":None,"senha":None}

page=st.sidebar.selectbox("Selecione a página",["Cadastro","Seu Perfil","Reservas","Minhas Reservas"])

if page =="Cadastro":
    st.title("SEU CADASTRO")
    
    st.session_state.usu_reserv["nome"]=st.text_input("Nome:",value=st.session_state.usu_reserv ["nome"] or"")
    st.session_state.usu_reserv["email"]=st.text_input("Email:",value=st.session_state.usu_reserv ["email"] or"")
    st.session_state.usu_reserv["senha"]=st.text_input("Senha:",type="password",value=st.session_state.usu_reserv ["senha"] or"")
    
    if st.button("Cadastrar"):
        email = st.session_state.usu_reserv["email"]
        nome = st.session_state.usu_reserv["nome"]
        senha = st.session_state.usu_reserv["senha"]
        

        
        
        if len(nome) < 4:
            st.warning("Digite um nome com pelo menos 4 caracteres.")
        elif len(email) < 6:
            st.warning("Digite um e-mail válido.")
        elif len(senha) < 7:
            st.warning("Digite uma senha com pelo menos 7 caracteres.")
        else:
            st.success("Suas credenciais foram cadastradas com sucesso!")
            st.experimental_set_query_params(page="Reservas")
            st.switch_page("Reservas")
        
            
            
            
elif page=="Seu Perfil":
    st.title("SEU PERFIL")
    if all(st.session_state.usu_reserv.values()):
        st.write("Nome:",st.session_state.usu_reserv["nome"])
        st.write("Email:",st.session_state.usu_reserv["email"])
        
    else:
        st.warning("Faça o Cadastro Primeiro")
        
        
        
        
        
    
    
    
elif page == "Reservas":
    st.title("Controle de Reservas")
    
    
    if not all(st.session_state.usu_reserv.values()):
        st.warning("Por favor, faça o cadastro antes de acessar as reservas.")
    else:
        st.write(f"Bem-vindo(a), {st.session_state.usu_reserv['nome']}!")
        
        
        if "reservations" not in st.session_state:
            st.session_state.reservations = []
        
        
        available_rooms = ["Auditório", "Laboratorio", "Blibioteca","Sala ds1","Sala sist1","Sala agn1","Sala adm1"]
        
        
        if st.session_state.reservations:
            st.subheader("Reservas Feitas:")
            for res in st.session_state.reservations:
                st.write(f"Sala: {res['room']} - Data: {res['date']} - Horário: {res['time']}")
        else:
            st.write("Nenhuma reserva feita ainda.")
        
        
        st.subheader("Nova Reserva")
        
        room = st.selectbox("Escolha uma sala", available_rooms)
        date = st.date_input("Escolha a data", min_value=datetime.date.today())
        motivo=st.text_input("diga o motivo")
        
        
        time_input = st.text_input("Digite o horário (formato HH:MM)", "09:00")
        
        
        try:
            time = datetime.datetime.strptime(time_input, "%H:%M").time()
        except ValueError:
            st.warning("Formato de hora inválido! Utilize o formato HH:MM (ex: 14:30).")
            time = None
        
        if st.button("Reservar"):
            if time:
               
                reservation_exists = False
                for res in st.session_state.reservations:
                    if res["room"] == room and res["date"] == str(date) and res["time"] == str(time):
                        reservation_exists = True
                        break
            
                if reservation_exists:
                    st.warning("Esta sala já está reservada nesse horário.")
                else:
                    
                  st.session_state.reservations.append({
                        "room": room,
                        "date": str(date),
                        "time": str(time),
                        "reason": motivo
                    })
                st.success(f"Sala {room} reservada para {date} às {time}. Motivo: {motivo}")
            else:
                st.warning("Por favor, insira uma hora válida.")
    
    
    
    
    
    

elif page == "Minhas Reservas":
    st.title("Controle de Reservas")
    
    
    if not all(st.session_state.usu_reserv.values()):
        st.warning("Por favor, faça o cadastro antes de acessar as reservas.")
    else:
        st.write(f"Bem-vindo(a), {st.session_state.usu_reserv['nome']}!")
        
        
        if "reservations" not in st.session_state:
            st.session_state.reservations = []
        
        
        available_rooms = ["Auditório", "Laboratorio", "Blibioteca","Sala ds1","Sala sist1","Sala agn1","Sala adm1"]
        
        
        if st.session_state.reservations:
            st.subheader("Reservas Feitas:")
            for res in st.session_state.reservations:
                st.write(f"Sala: {res['room']} - Data: {res['date']} - Horário: {res['time']}")
        else:
            st.write("Nenhuma reserva feita ainda.")
        
              