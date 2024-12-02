import streamlit as st
import datetime

# Conectando no CSS


# Inicializando variáveis no session_state
if "usu_reserv" not in st.session_state:
    st.session_state.usu_reserv = {"nome": None, "email": None, "senha": None}
if "reservations" not in st.session_state:
    st.session_state.reservations = []
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True  # Inicialmente logado após cadastro.

# Função de logout
def logout():
    st.session_state.logged_in = False
    st.session_state.usu_reserv = {"nome": None, "email": None, "senha": None}
    st.session_state.reservations = []
    st.experimental_rerun()

# Imagens associadas aos locais
images = {
    "Auditório": "https://www.architectus.com.br/wp-content/uploads/2023/03/170522_Escola_Profissionalizante_005-1.jpg",
    "Laboratório": "https://www.fasipe.com.br/upload/mod_galerias/131/5bfbe2e39f75c.JPG",
    "Biblioteca": "https://via.placeholder.com/150?text=Biblioteca",
    "Sala ds1": "https://via.placeholder.com/150?text=Sala+ds1",
    "Sala sist1": "https://via.placeholder.com/150?text=Sala+sist1",
    "Sala agn1": "https://via.placeholder.com/150?text=Sala+agn1",
    "Sala adm1": "https://via.placeholder.com/150?text=Sala+adm1",
}

# Verificar se o usuário está logado
if st.session_state.logged_in:
    # Menu lateral e botão de sair
    page = st.sidebar.selectbox(
        "Selecione a página", ["Cadastro", "Seu Perfil", "Reservas", "Minhas Reservas"]
    )
    if st.sidebar.button("Sair"):
        logout()

    # Mostrar reservas na barra lateral
    st.sidebar.subheader("Suas Reservas:")
    if st.session_state.reservations:
        for res in st.session_state.reservations:
            st.sidebar.write(f"**{res['room']}** - {res['date']} {res['time']}")
            st.sidebar.write(f"Motivo: {res['reason']}")
            st.sidebar.image(images.get(res["room"], "https://via.placeholder.com/150"))

    # Página Cadastro
    if page == "Cadastro":
        st.title("SEU CADASTRO")
        st.session_state.usu_reserv["nome"] = st.text_input(
            "Nome:", value=st.session_state.usu_reserv["nome"] or ""
        )
        st.session_state.usu_reserv["email"] = st.text_input(
            "Email:", value=st.session_state.usu_reserv["email"] or ""
        )
        st.session_state.usu_reserv["senha"] = st.text_input(
            "Senha:", type="password", value=st.session_state.usu_reserv["senha"] or ""
        )

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

    # Página Seu Perfil
    elif page == "Seu Perfil":
        st.title("SEU PERFIL")
        if all(st.session_state.usu_reserv.values()):
            st.write("Nome:", st.session_state.usu_reserv["nome"])
            st.write("Email:", st.session_state.usu_reserv["email"])
        else:
            st.warning("Faça o Cadastro Primeiro")

    # Página Reservas
    elif page == "Reservas":
        st.title("Controle de Reservas")

        if not all(st.session_state.usu_reserv.values()):
            st.warning("Por favor, faça o cadastro antes de acessar as reservas.")
        else:
            st.write(f"Bem-vindo(a), {st.session_state.usu_reserv['nome']}!")

            available_rooms = [
                "Auditório",
                "Laboratório",
                "Biblioteca",
                "Sala ds1",
                "Sala sist1",
                "Sala agn1",
                "Sala adm1",
            ]

            if st.session_state.reservations:
                st.subheader("Reservas Feitas:")
                for res in st.session_state.reservations:
                    st.write(
                        f"Sala: {res['room']} - Data: {res['date']} - Horário: {res['time']} - Motivo: {res['reason']}"
                    )
            else:
                st.write("Nenhuma reserva feita ainda.")

            st.subheader("Nova Reserva")
            room = st.selectbox("Escolha uma sala", available_rooms)
            date = st.date_input("Escolha a data", min_value=datetime.date.today())
            motivo = st.text_input("Diga o motivo")
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
                        if (
                            res["room"] == room
                            and res["date"] == str(date)
                            and res["time"] == str(time)
                        ):
                            reservation_exists = True
                            break

                    if reservation_exists:
                        st.warning("Esta sala já está reservada nesse horário.")
                    else:
                        st.session_state.reservations.append(
                            {
                                "room": room,
                                "date": str(date),
                                "time": str(time),
                                "reason": motivo,
                            }
                        )
                        st.success(
                            f"Sala {room} reservada para {date} às {time}. Motivo: {motivo}"
                        )
                else:
                    st.warning("Por favor, insira uma hora válida.")

    elif page == "Minhas Reservas":
        st.title("Minhas Reservas")

        if st.session_state.reservations:
            st.subheader("Reservas Feitas:")
            for res in st.session_state.reservations:
                st.write(
                    f"Sala: {res['room']} - Data: {res['date']} - Horário: {res['time']} - Motivo: {res['reason']}"
                )
                st.image(images.get(res["room"], "https://via.placeholder.com/150"))
        else:
            st.write("Nenhuma reserva feita ainda.")

else:
    
    st.title("Bem-vindo!")
    st.write("Você saiu da conta. Por favor, realize o cadastro novamente ou faça login.")