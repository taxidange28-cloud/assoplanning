import streamlit as st
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="ASSO-PLAN",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé
st.markdown("""
<style>
    .stApp { background-color: #f1f5f9; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stat-card {
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stat-card-green { background: #ecfdf5; }
    .stat-card-amber { background: #fffbeb; }
    .stat-card-gray { background: #f1f5f9; border: 1px solid #e2e8f0; }
    .stat-card-blue { background: #eff6ff; }
    
    .course-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# BASE DE DONNÉES UTILISATEURS - 40+ CHEFS D'ENTREPRISE
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

if "courses" not in st.session_state:
    st.session_state.courses = [
        {
            "id": 1,
            "depart": "Chartres Centre",
            "destination": "Aéroport Paris-Orly",
            "date": "2025-12-03",
            "heure": "06:30",
            "passagers": 2,
            "prix": "120€",
            "depose_par": "taxidange28@gmail.com",
            "depose_par_nom": "Transport DanGE",
            "commentaire": "Client régulier - Vol Air France 7h45",
            "statut": "disponible",
            "prise_par": None,
            "prise_par_nom": None,
            "horodatage_prise": None
        },
        {
            "id": 2,
            "depart": "Dreux Gare SNCF",
            "destination": "Chartres CHR",
            "date": "2025-12-03",
            "heure": "14:00",
            "passagers": 1,
            "prix": "45€",
            "depose_par": "taxi.dreux01@assoplan.fr",
            "depose_par_nom": "Dupont Taxi Dreux",
            "commentaire": "Patient - PMR",
            "statut": "disponible",
            "prise_par": None,
            "prise_par_nom": None,
            "horodatage_prise": None
        },
        {
            "id": 3,
            "depart": "Illiers-Combray",
            "destination": "Paris Gare Montparnasse",
            "date": "2025-12-04",
            "heure": "05:00",
            "passagers": 3,
            "prix": "150€",
            "depose_par": "taxidange28@gmail.com",
            "depose_par_nom": "Transport DanGE",
            "commentaire": "TGV 6h15 - Bagages volumineux",
            "statut": "prise",
            "prise_par": "taxi.chartres01@assoplan.fr",
            "prise_par_nom": "Taxi Martin Chartres",
            "horodatage_prise": "2025-12-02 10:23:45"
        },
        {
            "id": 4,
            "depart": "Nogent-le-Rotrou",
            "destination": "Chartres Clinique",
            "date": "2025-12-05",
            "heure": "08:00",
            "passagers": 1,
            "prix": "65€",
            "depose_par": "taxi.nogent01@assoplan.fr",
            "depose_par_nom": "Blanc Taxi Nogent",
            "commentaire": "RDV médical - retour prévu 11h",
            "statut": "disponible",
            "prise_par": None,
            "prise_par_nom": None,
            "horodatage_prise": None
        },
        {
            "id": 5,
            "depart": "Châteaudun Centre",
            "destination": "Paris CDG Terminal 2",
            "date": "2025-12-06",
            "heure": "04:30",
            "passagers": 4,
            "prix": "180€",
            "depose_par": "taxi.chateaudun01@assoplan.fr",
            "depose_par_nom": "Schmitt Taxi Châteaudun",
            "commentaire": "Vol 7h00 - 4 grosses valises",
            "statut": "disponible",
            "prise_par": None,
            "prise_par_nom": None,
            "horodatage_prise": None
        }
    ]

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================
def get_next_id():
    if not st.session_state.courses:
        return 1
    return max(c["id"] for c in st.session_state.courses) + 1

def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def get_courses_by_status(statut):
    return [c for c in st.session_state.courses if c["statut"] == statut]

def get_my_courses(email):
    return [c for c in st.session_state.courses if c["depose_par"] == email or c["prise_par"] == email]

# =============================================================================
# PAGE DE CONNEXION
# =============================================================================
def show_login():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0;">
        <div style="font-size: 4rem;">🚖</div>
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1e293b; margin: 10px 0;">ASSO-PLAN</h1>
        <p style="color: #64748b; font-size: 1rem;">Planning partagé pour services de taxi - Eure-et-Loir</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px; color: #94a3b8; font-size: 0.8rem;">
            {len(USERS)} entreprises enregistrées dans le réseau
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# APPLICATION PRINCIPALE
# =============================================================================
def show_app():
    user = st.session_state.current_user
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 2.5rem;">🚖</div>
            <div>
                <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700; color: #1e293b;">ASSO-PLAN</h1>
                <p style="margin: 0; color: #64748b;">{user['company']} - {user.get('zone', '')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right;">
            <p style="margin: 0; font-weight: 600; color: #1e293b;">{user['name']}</p>
            <p style="margin: 0; color: #64748b; font-size: 0.85rem;">{'👑 Administrateur' if user['is_admin'] else '🚖 Chauffeur'}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Déconnexion", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    
    st.markdown("---")
    
    # Statistiques
    disponibles = get_courses_by_status("disponible")
    prises = get_courses_by_status("prise")
    terminees = get_courses_by_status("terminee")
    mes_courses = get_my_courses(user["email"])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card stat-card-green">
            <p style="font-size: 2.5rem; font-weight: 700; color: #059669; margin: 0;">{len(disponibles)}</p>
            <p style="color: #64748b; margin: 5px 0 0 0;">Disponibles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card stat-card-amber">
            <p style="font-size: 2.5rem; font-weight: 700; color: #d97706; margin: 0;">{len(prises)}</p>
            <p style="color: #64748b; margin: 5px 0 0 0;">En cours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card stat-card-gray">
            <p style="font-size: 2.5rem; font-weight: 700; color: #475569; margin: 0;">{len(terminees)}</p>
            <p style="color: #64748b; margin: 5px 0 0 0;">Terminées</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card stat-card-blue">
            <p style="font-size: 2.5rem; font-weight: 700; color: #2563eb; margin: 0;">{len(mes_courses)}</p>
            <p style="color: #64748b; margin: 5px 0 0 0;">Mes courses</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton nouvelle course
    col1, col2 = st.columns([3, 1])
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
                        st.session_state.courses.insert(0, new_course)
                        st.session_state.show_new_course = False
                        st.success("✅ Course déposée avec succès !")
                        st.rerun()
                    else:
                        st.error("⚠️ Veuillez remplir le départ et la destination")
    
    # Onglets
    tab_labels = ["🟢 Disponibles", "🟡 En cours", "✅ Terminées", "📋 Mes courses"]
    if user["is_admin"]:
        tab_labels.append("👑 Admin")
    
    tabs = st.tabs(tab_labels)
    
    with tabs[0]:
        show_courses_list(disponibles, user)
    
    with tabs[1]:
        show_courses_list(prises, user)
    
    with tabs[2]:
        show_courses_list(terminees, user)
    
    with tabs[3]:
        show_courses_list(mes_courses, user)
    
    if user["is_admin"]:
        with tabs[4]:
            st.markdown(f"**{len(USERS)} entreprises enregistrées** | **{len(st.session_state.courses)} courses au total**")
            show_courses_list(st.session_state.courses, user)
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p>ASSO-PLAN © 2025 — Planning partagé pour services de taxi</p>
        <p style="font-size: 0.8rem;">Développé pour Transport DanGE / agitaxi.fr | {len(USERS)} entreprises dans le réseau</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# AFFICHAGE DES COURSES
# =============================================================================
def show_courses_list(courses_list, user):
    if not courses_list:
        st.info("📭 Aucune course dans cette catégorie")
        return
    
    for course in courses_list:
        # Couleurs selon statut
        if course["statut"] == "disponible":
            border_color = "#10b981"
            status_bg = "#ecfdf5"
            status_color = "#059669"
            status_text = "🟢 Disponible"
        elif course["statut"] == "prise":
            border_color = "#f59e0b"
            status_bg = "#fffbeb"
            status_color = "#d97706"
            status_text = "🟡 Prise"
        else:
            border_color = "#94a3b8"
            status_bg = "#f1f5f9"
            status_color = "#64748b"
            status_text = "✅ Terminée"
        
        # Affichage de la carte
        st.markdown(f"""
        <div style="background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; 
                    border: 1px solid #e2e8f0; border-left: 4px solid {border_color};">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="background: {status_bg}; color: {status_color}; padding: 5px 12px; 
                                 border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                        {status_text}
                    </span>
                    <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 8px;">Déposée par {course['depose_par_nom']}</p>
                </div>
                <div style="text-align: right;">
                    <p style="font-size: 1.4rem; font-weight: 700; color: #1e293b; margin: 0;">{course['prix'] or '—'}</p>
                    <p style="color: #64748b; font-size: 0.85rem; margin: 0;">{course['passagers']} passager(s)</p>
                </div>
            </div>
            
            <div style="margin: 15px 0;">
                <p style="font-size: 1.1rem; font-weight: 600; color: #1e293b; margin: 5px 0;">
                    🟢 {course['depart']}
                </p>
                <p style="color: #94a3b8; margin: 0 0 0 10px;">↓</p>
                <p style="font-size: 1.1rem; font-weight: 600; color: #1e293b; margin: 5px 0;">
                    🔴 {course['destination']}
                </p>
            </div>
            
            <p style="color: #64748b; font-size: 0.9rem;">
                📅 {format_date(course['date'])} &nbsp;&nbsp; 🕐 <strong style="color: #2563eb;">{course['heure']}</strong>
            </p>
            
            {"<p style='background: #f8fafc; padding: 10px; border-radius: 8px; color: #475569; font-size: 0.85rem; margin-top: 10px;'>💬 " + course['commentaire'] + "</p>" if course['commentaire'] else ""}
            
            {"<p style='background: #fffbeb; padding: 10px; border-radius: 8px; color: #92400e; font-size: 0.85rem; margin-top: 10px;'><strong>Prise par:</strong> " + str(course['prise_par_nom'] or '') + "<br><small>⏱️ " + str(course['horodatage_prise'] or '') + "</small></p>" if course['statut'] != 'disponible' and course['prise_par_nom'] else ""}
        </div>
        """, unsafe_allow_html=True)
        
        # Boutons d'action
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        # Prendre la course
        if course["statut"] == "disponible" and course["depose_par"] != user["email"]:
            with col1:
                if st.button(f"✅ JE PRENDS", key=f"take_{course['id']}"):
                    for c in st.session_state.courses:
                        if c["id"] == course["id"]:
                            c["statut"] = "prise"
                            c["prise_par"] = user["email"]
                            c["prise_par_nom"] = user["company"]
                            c["horodatage_prise"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("✅ Course prise !")
                    st.rerun()
        
        # Actions si prise par moi
        if course["statut"] == "prise" and course["prise_par"] == user["email"]:
            with col1:
                if st.button(f"🏁 Terminer", key=f"finish_{course['id']}"):
                    for c in st.session_state.courses:
                        if c["id"] == course["id"]:
                            c["statut"] = "terminee"
                    st.success("✅ Course terminée !")
                    st.rerun()
            with col2:
                if st.button(f"↩️ Annuler", key=f"cancel_{course['id']}"):
                    for c in st.session_state.courses:
                        if c["id"] == course["id"]:
                            c["statut"] = "disponible"
                            c["prise_par"] = None
                            c["prise_par_nom"] = None
                            c["horodatage_prise"] = None
                    st.success("↩️ Course remise en disponibilité")
                    st.rerun()
        
        # Actions Admin
        if user["is_admin"]:
            if course["statut"] == "prise":
                with col3:
                    if st.button(f"🔄 Réattribuer", key=f"reassign_{course['id']}"):
                        for c in st.session_state.courses:
                            if c["id"] == course["id"]:
                                c["statut"] = "disponible"
                                c["prise_par"] = None
                                c["prise_par_nom"] = None
                                c["horodatage_prise"] = None
                        st.success("🔄 Course réattribuée")
                        st.rerun()
            with col4:
                if st.button(f"🗑️ Suppr.", key=f"delete_{course['id']}"):
                    st.session_state.courses = [c for c in st.session_state.courses if c["id"] != course["id"]]
                    st.success("🗑️ Course supprimée")
                    st.rerun()
        
        # Badge propriétaire
        if course["depose_par"] == user["email"]:
            with col5:
                st.markdown("📌 **Ma course**")
        
        st.markdown("<br>", unsafe_allow_html=True)

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
