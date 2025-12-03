import streamlit as st
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

# Configuration de la page
st.set_page_config(
    page_title="ASSO-PLAN",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# CONNEXION GOOGLE SHEETS
# =============================================================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_google_sheet():
    """Connexion au Google Sheet"""
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    spreadsheet_id = st.secrets["google_sheets"]["spreadsheet_id"]
    sheet = client.open_by_key(spreadsheet_id).sheet1
    return sheet

def load_courses_from_sheet():
    """Charge toutes les courses depuis Google Sheets"""
    try:
        sheet = get_google_sheet()
        records = sheet.get_all_records()
        courses = []
        for record in records:
            course = {
                "id": int(record.get("id", 0)),
                "depart": str(record.get("depart", "")),
                "destination": str(record.get("destination", "")),
                "date": str(record.get("date", "")),
                "heure": str(record.get("heure", "")),
                "passagers": int(record.get("passagers", 1)) if record.get("passagers") else 1,
                "prix": str(record.get("prix", "")),
                "depose_par": str(record.get("depose_par", "")),
                "depose_par_nom": str(record.get("depose_par_nom", "")),
                "commentaire": str(record.get("commentaire", "")),
                "statut": str(record.get("statut", "disponible")),
                "prise_par": str(record.get("prise_par", "")) if record.get("prise_par") else None,
                "prise_par_nom": str(record.get("prise_par_nom", "")) if record.get("prise_par_nom") else None,
                "horodatage_prise": str(record.get("horodatage_prise", "")) if record.get("horodatage_prise") else None
            }
            if course["id"] > 0:
                courses.append(course)
        return courses
    except Exception as e:
        st.error(f"Erreur de chargement: {e}")
        return []

def save_course_to_sheet(course):
    """Ajoute une nouvelle course dans Google Sheets"""
    try:
        sheet = get_google_sheet()
        row = [
            course["id"],
            course["depart"],
            course["destination"],
            course["date"],
            course["heure"],
            course["passagers"],
            course["prix"],
            course["depose_par"],
            course["depose_par_nom"],
            course["commentaire"],
            course["statut"],
            course["prise_par"] or "",
            course["prise_par_nom"] or "",
            course["horodatage_prise"] or ""
        ]
        sheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Erreur de sauvegarde: {e}")
        return False

def update_course_in_sheet(course_id, updates):
    """Met à jour une course dans Google Sheets"""
    try:
        sheet = get_google_sheet()
        # Trouver la ligne avec cet ID
        cell = sheet.find(str(course_id), in_column=1)
        if cell:
            row_number = cell.row
            # Mettre à jour les colonnes nécessaires
            if "statut" in updates:
                sheet.update_cell(row_number, 11, updates["statut"])
            if "prise_par" in updates:
                sheet.update_cell(row_number, 12, updates["prise_par"] or "")
            if "prise_par_nom" in updates:
                sheet.update_cell(row_number, 13, updates["prise_par_nom"] or "")
            if "horodatage_prise" in updates:
                sheet.update_cell(row_number, 14, updates["horodatage_prise"] or "")
            return True
    except Exception as e:
        st.error(f"Erreur de mise à jour: {e}")
    return False

def delete_course_from_sheet(course_id):
    """Supprime une course de Google Sheets"""
    try:
        sheet = get_google_sheet()
        cell = sheet.find(str(course_id), in_column=1)
        if cell:
            sheet.delete_rows(cell.row)
            return True
    except Exception as e:
        st.error(f"Erreur de suppression: {e}")
    return False

def get_next_id():
    """Obtient le prochain ID disponible"""
    courses = load_courses_from_sheet()
    if not courses:
        return 1
    return max(c["id"] for c in courses) + 1

# =============================================================================
# BASE DE DONNÉES UTILISATEURS - 43 CHEFS D'ENTREPRISE
# =============================================================================
USERS = {
    # ADMINISTRATEURS
    "taxidange28@gmail.com": {
        "password": "test123",
        "name": "Dunois - Transport DanGE",
        "company": "Transport DanGE",
        "is_admin": True,
        "zone": "Chartres"
    },
    "taxidange@gmail.com": {
        "password": "test123",
        "name": "Chauffeur DanGE 1",
        "company": "Transport DanGE",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxidangeau@gmail.com": {
        "password": "test123",
        "name": "Chauffeur DanGE 2",
        "company": "Transport DanGE",
        "is_admin": False,
        "zone": "Chartres"
    },
    
    # ZONE CHARTRES (10 entreprises)
    "taxi.chartres01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Jean MARTIN",
        "company": "Taxi Martin Chartres",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Pierre DUBOIS",
        "company": "Dubois Transports",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Marie LEROY",
        "company": "Taxi Leroy",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres04@assoplan.fr": {
        "password": "assoplan2025",
        "name": "François MOREAU",
        "company": "Moreau VTC",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres05@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Sophie BERNARD",
        "company": "Bernard Taxi Services",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres06@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Michel PETIT",
        "company": "Petit Express",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres07@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Catherine ROUX",
        "company": "Roux Mobilité",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres08@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Philippe FOURNIER",
        "company": "Fournier Transports",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres09@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Nathalie GIRARD",
        "company": "Girard Taxi 28",
        "is_admin": False,
        "zone": "Chartres"
    },
    "taxi.chartres10@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Laurent BONNET",
        "company": "Bonnet Services",
        "is_admin": False,
        "zone": "Chartres"
    },
    
    # ZONE DREUX (10 entreprises)
    "taxi.dreux01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Alain DUPONT",
        "company": "Dupont Taxi Dreux",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Isabelle LAMBERT",
        "company": "Lambert Express",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Bruno FONTAINE",
        "company": "Fontaine Transports",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux04@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Sylvie ROUSSEAU",
        "company": "Rousseau Mobilité",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux05@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Christophe VINCENT",
        "company": "Vincent Taxi Services",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux06@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Sandrine MULLER",
        "company": "Muller Transport",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux07@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Thierry LEFEVRE",
        "company": "Lefevre Express Dreux",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux08@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Valérie FAURE",
        "company": "Faure Taxi",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux09@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Pascal ANDRE",
        "company": "Andre Transports",
        "is_admin": False,
        "zone": "Dreux"
    },
    "taxi.dreux10@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Caroline MERCIER",
        "company": "Mercier Services",
        "is_admin": False,
        "zone": "Dreux"
    },
    
    # ZONE NOGENT-LE-ROTROU (5 entreprises)
    "taxi.nogent01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Didier BLANC",
        "company": "Blanc Taxi Nogent",
        "is_admin": False,
        "zone": "Nogent-le-Rotrou"
    },
    "taxi.nogent02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Martine GUERIN",
        "company": "Guerin Transports",
        "is_admin": False,
        "zone": "Nogent-le-Rotrou"
    },
    "taxi.nogent03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Yves BOYER",
        "company": "Boyer Express",
        "is_admin": False,
        "zone": "Nogent-le-Rotrou"
    },
    "taxi.nogent04@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Annick GARNIER",
        "company": "Garnier Mobilité",
        "is_admin": False,
        "zone": "Nogent-le-Rotrou"
    },
    "taxi.nogent05@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Gérard CHEVALIER",
        "company": "Chevalier Taxi",
        "is_admin": False,
        "zone": "Nogent-le-Rotrou"
    },
    
    # ZONE CHATEAUDUN (5 entreprises)
    "taxi.chateaudun01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Olivier SCHMITT",
        "company": "Schmitt Taxi Châteaudun",
        "is_admin": False,
        "zone": "Châteaudun"
    },
    "taxi.chateaudun02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Dominique LEMAIRE",
        "company": "Lemaire Express",
        "is_admin": False,
        "zone": "Châteaudun"
    },
    "taxi.chateaudun03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Pascale HENRY",
        "company": "Henry Transports",
        "is_admin": False,
        "zone": "Châteaudun"
    },
    "taxi.chateaudun04@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Serge ROUSSEL",
        "company": "Roussel Services",
        "is_admin": False,
        "zone": "Châteaudun"
    },
    "taxi.chateaudun05@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Monique DAVID",
        "company": "David Taxi",
        "is_admin": False,
        "zone": "Châteaudun"
    },
    
    # ZONE ILLIERS-COMBRAY (5 entreprises)
    "taxi.illiers01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Eric BERTRAND",
        "company": "Bertrand Taxi Illiers",
        "is_admin": False,
        "zone": "Illiers-Combray"
    },
    "taxi.illiers02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Brigitte MOREL",
        "company": "Morel Express",
        "is_admin": False,
        "zone": "Illiers-Combray"
    },
    "taxi.illiers03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Franck LAURENT",
        "company": "Laurent Transports",
        "is_admin": False,
        "zone": "Illiers-Combray"
    },
    "taxi.illiers04@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Céline SIMON",
        "company": "Simon Mobilité",
        "is_admin": False,
        "zone": "Illiers-Combray"
    },
    "taxi.illiers05@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Patrick MICHEL",
        "company": "Michel Taxi Services",
        "is_admin": False,
        "zone": "Illiers-Combray"
    },
    
    # ZONE MAINTENON / EPERNON (5 entreprises)
    "taxi.maintenon01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Stéphane GARCIA",
        "company": "Garcia Taxi Maintenon",
        "is_admin": False,
        "zone": "Maintenon"
    },
    "taxi.maintenon02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Véronique MARTINEZ",
        "company": "Martinez Express",
        "is_admin": False,
        "zone": "Maintenon"
    },
    "taxi.epernon01@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Nicolas LOPEZ",
        "company": "Lopez Transports Epernon",
        "is_admin": False,
        "zone": "Epernon"
    },
    "taxi.epernon02@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Aurélie GONZALEZ",
        "company": "Gonzalez Taxi",
        "is_admin": False,
        "zone": "Epernon"
    },
    "taxi.epernon03@assoplan.fr": {
        "password": "assoplan2025",
        "name": "Jérôme WILSON",
        "company": "Wilson Services",
        "is_admin": False,
        "zone": "Epernon"
    },
}

# =============================================================================
# INITIALISATION DE LA SESSION
# =============================================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.show_new_course = False

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def get_courses_by_status(courses, statut):
    return [c for c in courses if c["statut"] == statut]

def get_my_courses(courses, email):
    return [c for c in courses if c["depose_par"] == email or c["prise_par"] == email]

# =============================================================================
# PAGE DE CONNEXION
# =============================================================================
def show_login():
    st.title("🚖 ASSO-PLAN")
    st.subheader("Planning partagé pour services de taxi - Eure-et-Loir")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Connexion")
        
        email = st.text_input("Email", placeholder="votre@email.fr", key="login_email")
        password = st.text_input("Mot de passe", type="password", placeholder="••••••••", key="login_password")
        
        if st.button("Se connecter", type="primary", use_container_width=True):
            email_lower = email.lower().strip()
            if email_lower in USERS and USERS[email_lower]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = {
                    "email": email_lower,
                    "name": USERS[email_lower]["name"],
                    "company": USERS[email_lower]["company"],
                    "is_admin": USERS[email_lower]["is_admin"],
                    "zone": USERS[email_lower].get("zone", "")
                }
                st.rerun()
            else:
                st.error("❌ Email ou mot de passe incorrect")
        
        st.markdown("---")
        
        with st.expander("📋 Comptes de démonstration"):
            st.markdown("""
            **Compte Admin :**
            - `taxidange28@gmail.com` / `test123`
            
            **Comptes Chauffeurs :**
            - `taxidange@gmail.com` / `test123`
            - `taxidangeau@gmail.com` / `test123`
            
            **Autres entreprises (40+) :**
            - `taxi.chartres01@assoplan.fr` / `assoplan2025`
            - `taxi.dreux01@assoplan.fr` / `assoplan2025`
            - `taxi.nogent01@assoplan.fr` / `assoplan2025`
            - etc.
            """)
        
        st.info(f"📊 {len(USERS)} entreprises enregistrées dans le réseau")

# =============================================================================
# APPLICATION PRINCIPALE
# =============================================================================
def show_app():
    user = st.session_state.current_user
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🚖 ASSO-PLAN")
        st.caption(f"{user['company']} - {user.get('zone', '')}")
    
    with col2:
        st.markdown(f"**{user['name']}**")
        st.caption("👑 Administrateur" if user["is_admin"] else "🚖 Chauffeur")
        if st.button("🚪 Déconnexion", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    
    st.markdown("---")
    
    # Charger les courses depuis Google Sheets
    courses = load_courses_from_sheet()
    
    # Statistiques
    disponibles = get_courses_by_status(courses, "disponible")
    prises = get_courses_by_status(courses, "prise")
    terminees = get_courses_by_status(courses, "terminee")
    mes_courses = get_my_courses(courses, user["email"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="🟢 Disponibles", value=len(disponibles))
    
    with col2:
        st.metric(label="🟡 En cours", value=len(prises))
    
    with col3:
        st.metric(label="✅ Terminées", value=len(terminees))
    
    with col4:
        st.metric(label="📋 Mes courses", value=len(mes_courses))
    
    st.markdown("---")
    
    # Boutons d'action
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🔄 Rafraîchir les données", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()
    with col2:
        if st.button("➕ Déposer une course", type="primary", use_container_width=True):
            st.session_state.show_new_course = True
    
    # Formulaire nouvelle course
    if st.session_state.show_new_course:
        with st.expander("📝 Nouvelle course", expanded=True):
            with st.form("new_course_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    depart = st.text_input("Lieu de départ *", placeholder="Ex: Chartres Gare")
                with col2:
                    destination = st.text_input("Destination *", placeholder="Ex: Paris CDG")
                
                col1, col2 = st.columns(2)
                with col1:
                    date_course = st.date_input("Date *", value=datetime.now() + timedelta(days=1))
                with col2:
                    heure_course = st.time_input("Heure *", value=datetime.strptime("08:00", "%H:%M").time())
                
                col1, col2 = st.columns(2)
                with col1:
                    passagers = st.number_input("Passagers", min_value=1, max_value=9, value=1)
                with col2:
                    prix = st.text_input("Prix proposé", placeholder="Ex: 80€")
                
                commentaire = st.text_area("Commentaire", placeholder="Infos complémentaires (PMR, bagages, etc.)")
                
                col1, col2 = st.columns(2)
                with col1:
                    annuler = st.form_submit_button("Annuler", use_container_width=True)
                with col2:
                    deposer = st.form_submit_button("Déposer", type="primary", use_container_width=True)
                
                if annuler:
                    st.session_state.show_new_course = False
                    st.rerun()
                
                if deposer:
                    if depart and destination:
                        new_course = {
                            "id": get_next_id(),
                            "depart": depart,
                            "destination": destination,
                            "date": date_course.strftime("%Y-%m-%d"),
                            "heure": heure_course.strftime("%H:%M"),
                            "passagers": passagers,
                            "prix": prix,
                            "depose_par": user["email"],
                            "depose_par_nom": user["company"],
                            "commentaire": commentaire,
                            "statut": "disponible",
                            "prise_par": None,
                            "prise_par_nom": None,
                            "horodatage_prise": None
                        }
                        if save_course_to_sheet(new_course):
                            st.session_state.show_new_course = False
                            st.success("✅ Course déposée avec succès !")
                            st.cache_resource.clear()
                            st.rerun()
                    else:
                        st.error("⚠️ Veuillez remplir le départ et la destination")
    
    # Onglets
    tab_labels = ["🟢 Disponibles", "🟡 En cours", "✅ Terminées", "📋 Mes courses"]
    if user["is_admin"]:
        tab_labels.append("👑 Admin")
    
    tabs = st.tabs(tab_labels)
    
    with tabs[0]:
        show_courses_list(disponibles, user, "dispo")
    
    with tabs[1]:
        show_courses_list(prises, user, "encours")
    
    with tabs[2]:
        show_courses_list(terminees, user, "term")
    
    with tabs[3]:
        show_courses_list(mes_courses, user, "mes")
    
    if user["is_admin"]:
        with tabs[4]:
            st.info(f"**{len(USERS)} entreprises enregistrées** | **{len(courses)} courses au total**")
            show_courses_list(courses, user, "admin")
    
    # Footer
    st.markdown("---")
    st.caption(f"ASSO-PLAN © 2025 — Planning partagé pour services de taxi | Développé pour Transport DanGE / agitaxi.fr | {len(USERS)} entreprises dans le réseau")

# =============================================================================
# AFFICHAGE DES COURSES
# =============================================================================
def show_courses_list(courses_list, user, tab_prefix):
    if not courses_list:
        st.info("📭 Aucune course dans cette catégorie")
        return
    
    for course in courses_list:
        unique_key = f"{tab_prefix}_{course['id']}"
        
        # Container pour chaque course
        with st.container():
            # Statut
            if course["statut"] == "disponible":
                st.success(f"🟢 **DISPONIBLE** — Déposée par {course['depose_par_nom']}")
            elif course["statut"] == "prise":
                st.warning(f"🟡 **EN COURS** — Déposée par {course['depose_par_nom']}")
            else:
                st.info(f"✅ **TERMINÉE** — Déposée par {course['depose_par_nom']}")
            
            # Trajet et détails
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### 🟢 {course['depart']}")
                st.markdown("⬇️")
                st.markdown(f"### 🔴 {course['destination']}")
            
            with col2:
                st.markdown(f"**📅 Date:** {format_date(course['date'])}")
                st.markdown(f"**🕐 Heure:** {course['heure']}")
                st.markdown(f"**👥 Passagers:** {course['passagers']}")
            
            with col3:
                st.markdown(f"### 💰 {course['prix'] or '—'}")
                if course["depose_par"] == user["email"]:
                    st.caption("📌 Ma course déposée")
            
            # Commentaire
            if course["commentaire"]:
                st.caption(f"💬 {course['commentaire']}")
            
            # Info prise
            if course["statut"] != "disponible" and course["prise_par_nom"]:
                st.warning(f"**Prise par:** {course['prise_par_nom']} — ⏱️ {course['horodatage_prise']}")
            
            # Boutons d'action
            col1, col2, col3, col4 = st.columns(4)
            
            # Prendre la course
            if course["statut"] == "disponible" and course["depose_par"] != user["email"]:
                with col1:
                    if st.button("✅ JE PRENDS", key=f"take_{unique_key}", type="primary"):
                        updates = {
                            "statut": "prise",
                            "prise_par": user["email"],
                            "prise_par_nom": user["company"],
                            "horodatage_prise": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        if update_course_in_sheet(course["id"], updates):
                            st.success("✅ Course prise !")
                            st.cache_resource.clear()
                            st.rerun()
            
            # Actions si prise par moi
            if course["statut"] == "prise" and course["prise_par"] == user["email"]:
                with col1:
                    if st.button("🏁 Terminer", key=f"finish_{unique_key}"):
                        updates = {"statut": "terminee"}
                        if update_course_in_sheet(course["id"], updates):
                            st.success("✅ Course terminée !")
                            st.cache_resource.clear()
                            st.rerun()
                with col2:
                    if st.button("↩️ Annuler ma prise", key=f"cancel_{unique_key}"):
                        updates = {
                            "statut": "disponible",
                            "prise_par": "",
                            "prise_par_nom": "",
                            "horodatage_prise": ""
                        }
                        if update_course_in_sheet(course["id"], updates):
                            st.success("↩️ Course remise en disponibilité")
                            st.cache_resource.clear()
                            st.rerun()
            
            # Actions Admin
            if user["is_admin"]:
                if course["statut"] == "prise":
                    with col3:
                        if st.button("🔄 Réattribuer", key=f"reassign_{unique_key}"):
                            updates = {
                                "statut": "disponible",
                                "prise_par": "",
                                "prise_par_nom": "",
                                "horodatage_prise": ""
                            }
                            if update_course_in_sheet(course["id"], updates):
                                st.success("🔄 Course réattribuée")
                                st.cache_resource.clear()
                                st.rerun()
                with col4:
                    if st.button("🗑️ Supprimer", key=f"delete_{unique_key}"):
                        if delete_course_from_sheet(course["id"]):
                            st.success("🗑️ Course supprimée")
                            st.cache_resource.clear()
                            st.rerun()
            
            st.markdown("---")

# =============================================================================
# POINT D'ENTRÉE
# =============================================================================
def main():
    if not st.session_state.logged_in:
        show_login()
    else:
        show_app()

if __name__ == "__main__":
    main()
