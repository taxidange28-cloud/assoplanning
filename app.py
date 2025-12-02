"""
ASSO-PLAN - Planning partagé pour services de taxi
Version Python avec Streamlit
Développé pour Transport DanGE / agitaxi.fr
"""

import streamlit as st
from datetime import datetime, timedelta
import json

# ============ CONFIGURATION PAGE ============
st.set_page_config(
    page_title="ASSO-PLAN",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ STYLES CSS PERSONNALISÉS ============
st.markdown("""
<style>
    /* Global */
    .stApp { background-color: #f1f5f9; }
    
    /* Header personnalisé */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
        padding: 20px 30px;
        border-radius: 16px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .header-subtitle {
        color: #93c5fd;
        font-size: 0.9rem;
        margin: 0;
    }
    .header-user {
        color: white;
        text-align: right;
    }
    .header-user-name {
        font-weight: 600;
        font-size: 1rem;
    }
    .header-user-role {
        color: #93c5fd;
        font-size: 0.85rem;
    }
    
    /* Stats cards */
    .stat-card {
        padding: 20px;
        border-radius: 16px;
        text-align: center;
    }
    .stat-card.green { background: #ecfdf5; }
    .stat-card.amber { background: #fffbeb; }
    .stat-card.gray { background: #f1f5f9; border: 1px solid #e2e8f0; }
    .stat-card.blue { background: #eff6ff; }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .stat-card.green .stat-number { color: #059669; }
    .stat-card.amber .stat-number { color: #d97706; }
    .stat-card.gray .stat-number { color: #475569; }
    .stat-card.blue .stat-number { color: #2563eb; }
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Course cards */
    .course-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        border-left: 4px solid;
    }
    .course-card.disponible { border-left-color: #10b981; }
    .course-card.prise { border-left-color: #f59e0b; }
    .course-card.terminee { border-left-color: #94a3b8; }
    
    .course-status {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .course-status.disponible { background: #ecfdf5; color: #059669; }
    .course-status.prise { background: #fffbeb; color: #d97706; }
    .course-status.terminee { background: #f1f5f9; color: #64748b; }
    
    .course-route {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin: 15px 0;
    }
    .course-arrow { color: #94a3b8; margin: 0 10px; }
    
    .course-info {
        display: flex;
        gap: 20px;
        color: #64748b;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    .course-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .course-comment {
        background: #f8fafc;
        padding: 12px;
        border-radius: 10px;
        color: #475569;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    .course-prise-info {
        background: #fffbeb;
        padding: 12px;
        border-radius: 10px;
        color: #92400e;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    .course-deposant {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 5px;
    }
    
    /* Login */
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        background: white;
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .login-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 10px;
    }
    .login-subtitle {
        text-align: center;
        color: #64748b;
        margin-bottom: 30px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.2s;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 12px;
        padding: 10px 20px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10b981 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============ DONNÉES UTILISATEURS ============
USERS = {
    'taxidange28@gmail.com': {
        'password': 'test123',
        'name': 'Transport DanGE (Admin)',
        'company': 'Transport DanGE',
        'is_admin': True
    },
    'taxidange@gmail.com': {
        'password': 'test123',
        'name': 'Chauffeur DanGE 1',
        'company': 'Transport DanGE',
        'is_admin': False
    },
    'taxidangeau@gmail.com': {
        'password': 'test123',
        'name': 'Chauffeur DanGE 2',
        'company': 'Transport DanGE',
        'is_admin': False
    },
    'taxi.chartres@demo.fr': {
        'password': 'test123',
        'name': 'Taxi Chartres',
        'company': 'Taxi Chartres SARL',
        'is_admin': False
    },
    'express.dreux@demo.fr': {
        'password': 'test123',
        'name': 'Express Dreux',
        'company': 'Express Dreux',
        'is_admin': False
    }
}

# ============ INITIALISATION SESSION ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

if 'courses' not in st.session_state:
    st.session_state.courses = [
        {
            'id': 1,
            'depart': 'Chartres Centre',
            'destination': 'Aéroport Paris-Orly',
            'date': '2025-12-03',
            'heure': '06:30',
            'passagers': 2,
            'prix': '120€',
            'depose_par': 'taxidange28@gmail.com',
            'depose_par_nom': 'Transport DanGE',
            'commentaire': 'Client régulier - Vol Air France 7h45',
            'statut': 'disponible',
            'prise_par': None,
            'prise_par_nom': None,
            'horodatage_prise': None
        },
        {
            'id': 2,
            'depart': 'Dreux Gare SNCF',
            'destination': 'Chartres CHR',
            'date': '2025-12-03',
            'heure': '14:00',
            'passagers': 1,
            'prix': '45€',
            'depose_par': 'express.dreux@demo.fr',
            'depose_par_nom': 'Express Dreux',
            'commentaire': 'Patient - PMR',
            'statut': 'disponible',
            'prise_par': None,
            'prise_par_nom': None,
            'horodatage_prise': None
        },
        {
            'id': 3,
            'depart': 'Illiers-Combray',
            'destination': 'Paris Gare Montparnasse',
            'date': '2025-12-04',
            'heure': '05:00',
            'passagers': 3,
            'prix': '150€',
            'depose_par': 'taxidange28@gmail.com',
            'depose_par_nom': 'Transport DanGE',
            'commentaire': 'TGV 6h15 - Bagages volumineux',
            'statut': 'prise',
            'prise_par': 'taxi.chartres@demo.fr',
            'prise_par_nom': 'Taxi Chartres SARL',
            'horodatage_prise': '2025-12-02 10:23:45'
        }
    ]

# ============ FONCTIONS UTILITAIRES ============
def get_next_id():
    if not st.session_state.courses:
        return 1
    return max(c['id'] for c in st.session_state.courses) + 1

def format_date(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%d/%m/%Y')
    except:
        return date_str

def get_courses_by_status(statut):
    return [c for c in st.session_state.courses if c['statut'] == statut]

def get_my_courses(email):
    return [c for c in st.session_state.courses 
            if c['depose_par'] == email or c['prise_par'] == email]

# ============ PAGE DE CONNEXION ============
def show_login():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <div style="font-size: 4rem;">🚖</div>
        <h1 style="font-size: 3rem; font-weight: 700; color: #1e293b; margin: 10px 0;">ASSO-PLAN</h1>
        <p style="color: #64748b; font-size: 1.1rem;">Planning partagé pour services de taxi</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("### 🔐 Connexion")
            
            email = st.text_input("Email", placeholder="votre@email.fr")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            
            if st.button("Se connecter", type="primary", use_container_width=True):
                email_lower = email.lower().strip()
                if email_lower in USERS and USERS[email_lower]['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        'email': email_lower,
                        **USERS[email_lower]
                    }
                    st.rerun()
                else:
                    st.error("❌ Email ou mot de passe incorrect")
            
            st.markdown("---")
            st.markdown("**Comptes de démonstration :**")
            st.markdown("""
            | Email | Rôle | Mot de passe |
            |-------|------|--------------|
            | `taxidange28@gmail.com` | 👑 Admin | `test123` |
            | `taxidange@gmail.com` | Chauffeur | `test123` |
            | `taxidangeau@gmail.com` | Chauffeur | `test123` |
            """)

# ============ APPLICATION PRINCIPALE ============
def show_app():
    user = st.session_state.current_user
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 2.5rem;">🚖</div>
            <div>
                <h1 style="margin: 0; font-size: 2rem; font-weight: 700; color: #1e293b;">ASSO-PLAN</h1>
                <p style="margin: 0; color: #64748b;">{user['company']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: right;">
            <p style="margin: 0; font-weight: 600; color: #1e293b;">{user['name']}</p>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">{'👑 Administrateur' if user['is_admin'] else '🚖 Chauffeur'}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Déconnexion"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()
    
    st.markdown("---")
    
    # Statistiques
    disponibles = get_courses_by_status('disponible')
    prises = get_courses_by_status('prise')
    terminees = get_courses_by_status('terminee')
    mes_courses = get_my_courses(user['email'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card green">
            <p class="stat-number">{len(disponibles)}</p>
            <p class="stat-label">Disponibles</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card amber">
            <p class="stat-number">{len(prises)}</p>
            <p class="stat-label">En cours</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card gray">
            <p class="stat-number">{len(terminees)}</p>
            <p class="stat-label">Terminées</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card blue">
            <p class="stat-number">{len(mes_courses)}</p>
            <p class="stat-label">Mes courses</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bouton nouvelle course
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Déposer une course", type="primary", use_container_width=True):
            st.session_state.show_new_course = True
    
    # Modal nouvelle course
    if st.session_state.get('show_new_course', False):
        with st.expander("📝 Nouvelle course", expanded=True):
            with st.form("new_course_form"):
                col1, col2 = st.columns(2)
                with col1:
                    depart = st.text_input("Lieu de départ *", placeholder="Ex: Chartres Gare")
                with col2:
                    destination = st.text_input("Destination *", placeholder="Ex: Paris CDG")
                
                col1, col2 = st.columns(2)
                with col1:
                    date = st.date_input("Date *", value=datetime.now() + timedelta(days=1))
                with col2:
                    heure = st.time_input("Heure *", value=datetime.strptime("08:00", "%H:%M").time())
                
                col1, col2 = st.columns(2)
                with col1:
                    passagers = st.number_input("Passagers", min_value=1, max_value=9, value=1)
                with col2:
                    prix = st.text_input("Prix proposé", placeholder="Ex: 80€")
                
                commentaire = st.text_area("Commentaire", placeholder="Infos complémentaires (PMR, bagages, etc.)")
                
                col1, col2 = st.columns(2)
                with col1:
                    cancel = st.form_submit_button("Annuler", use_container_width=True)
                with col2:
                    submit = st.form_submit_button("Déposer", type="primary", use_container_width=True)
                
                if cancel:
                    st.session_state.show_new_course = False
                    st.rerun()
                
                if submit:
                    if depart and destination:
                        new_course = {
                            'id': get_next_id(),
                            'depart': depart,
                            'destination': destination,
                            'date': date.strftime('%Y-%m-%d'),
                            'heure': heure.strftime('%H:%M'),
                            'passagers': passagers,
                            'prix': prix,
                            'depose_par': user['email'],
                            'depose_par_nom': user['company'],
                            'commentaire': commentaire,
                            'statut': 'disponible',
                            'prise_par': None,
                            'prise_par_nom': None,
                            'horodatage_prise': None
                        }
                        st.session_state.courses.insert(0, new_course)
                        st.session_state.show_new_course = False
                        st.success("✅ Course déposée avec succès !")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir le départ et la destination")
    
    # Onglets
    tabs_list = ["🟢 Disponibles", "🟡 En cours", "✅ Terminées", "📋 Mes courses"]
    if user['is_admin']:
        tabs_list.append("👑 Admin (Toutes)")
    
    tabs = st.tabs(tabs_list)
    
    # Onglet Disponibles
    with tabs[0]:
        show_courses_list(disponibles, user, "disponible")
    
    # Onglet En cours
    with tabs[1]:
        show_courses_list(prises, user, "prise")
    
    # Onglet Terminées
    with tabs[2]:
        show_courses_list(terminees, user, "terminee")
    
    # Onglet Mes courses
    with tabs[3]:
        show_courses_list(mes_courses, user, "mes")
    
    # Onglet Admin
    if user['is_admin']:
        with tabs[4]:
            show_courses_list(st.session_state.courses, user, "admin")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        <p>ASSO-PLAN © 2025 — Planning partagé pour services de taxi</p>
        <p style="font-size: 0.85rem;">Développé pour Transport DanGE / agitaxi.fr</p>
    </div>
    """, unsafe_allow_html=True)

# ============ AFFICHAGE DES COURSES ============
def show_courses_list(courses_list, user, context):
    if not courses_list:
        st.info("📭 Aucune course dans cette catégorie")
        return
    
    for course in courses_list:
        with st.container():
            # Status badge
            status_emoji = "🟢" if course['statut'] == 'disponible' else "🟡" if course['statut'] == 'prise' else "✅"
            status_label = "Disponible" if course['statut'] == 'disponible' else "Prise" if course['statut'] == 'prise' else "Terminée"
            status_color = "#ecfdf5" if course['statut'] == 'disponible' else "#fffbeb" if course['statut'] == 'prise' else "#f1f5f9"
            text_color = "#059669" if course['statut'] == 'disponible' else "#d97706" if course['statut'] == 'prise' else "#64748b"
            border_color = "#10b981" if course['statut'] == 'disponible' else "#f59e0b" if course['statut'] == 'prise' else "#94a3b8"
            
            st.markdown(f"""
            <div style="background: white; border-radius: 16px; padding: 20px; margin-bottom: 16px; 
                        border: 1px solid #e2e8f0; border-left: 4px solid {border_color};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div>
                        <span style="background: {status_color}; color: {text_color}; padding: 6px 14px; 
                                     border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">
                            {status_emoji} {status_label}
                        </span>
                        <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 8px;">Déposée par {course['depose_par_nom']}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0;">{course['prix'] or '—'}</p>
                        <p style="color: #64748b; font-size: 0.9rem; margin: 0;">{course['passagers']} pax</p>
                    </div>
                </div>
                
                <div style="margin: 20px 0;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="width: 12px; height: 12px; background: #10b981; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: #1e293b;">{course['depart']}</span>
                    </div>
                    <div style="margin-left: 5px; border-left: 2px dashed #e2e8f0; height: 15px;"></div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: #1e293b;">{course['destination']}</span>
                    </div>
                </div>
                
                <div style="display: flex; gap: 20px; color: #64748b; font-size: 0.9rem;">
                    <span>📅 {format_date(course['date'])}</span>
                    <span>🕐 <strong style="color: #2563eb; font-size: 1.1rem;">{course['heure']}</strong></span>
                </div>
                
                {'<div style="background: #f8fafc; padding: 12px; border-radius: 10px; margin-top: 15px; color: #475569; font-size: 0.9rem;">💬 ' + course['commentaire'] + '</div>' if course['commentaire'] else ''}
                
                {'<div style="background: #fffbeb; padding: 12px; border-radius: 10px; margin-top: 15px; color: #92400e; font-size: 0.9rem;"><strong>Prise par:</strong> ' + (course['prise_par_nom'] or '') + '<br><span style="font-size: 0.8rem;">Horodatage: ' + (course['horodatage_prise'] or '') + '</span></div>' if course['statut'] != 'disponible' and course['prise_par_nom'] else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Actions
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            
            # Bouton Prendre
            if course['statut'] == 'disponible' and course['depose_par'] != user['email']:
                with col1:
                    if st.button(f"✅ JE PRENDS", key=f"take_{course['id']}"):
                        for c in st.session_state.courses:
                            if c['id'] == course['id']:
                                c['statut'] = 'prise'
                                c['prise_par'] = user['email']
                                c['prise_par_nom'] = user['company']
                                c['horodatage_prise'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        st.success("✅ Course prise !")
                        st.rerun()
            
            # Actions si prise par moi
            if course['statut'] == 'prise' and course['prise_par'] == user['email']:
                with col1:
                    if st.button(f"🏁 Terminer", key=f"finish_{course['id']}"):
                        for c in st.session_state.courses:
                            if c['id'] == course['id']:
                                c['statut'] = 'terminee'
                        st.success("✅ Course terminée !")
                        st.rerun()
                with col2:
                    if st.button(f"↩️ Annuler", key=f"cancel_{course['id']}"):
                        for c in st.session_state.courses:
                            if c['id'] == course['id']:
                                c['statut'] = 'disponible'
                                c['prise_par'] = None
                                c['prise_par_nom'] = None
                                c['horodatage_prise'] = None
                        st.success("↩️ Course remise en disponibilité")
                        st.rerun()
            
            # Actions Admin
            if user['is_admin']:
                if course['statut'] == 'prise':
                    with col3:
                        if st.button(f"🔄 Réattribuer", key=f"reassign_{course['id']}"):
                            for c in st.session_state.courses:
                                if c['id'] == course['id']:
                                    c['statut'] = 'disponible'
                                    c['prise_par'] = None
                                    c['prise_par_nom'] = None
                                    c['horodatage_prise'] = None
                            st.success("🔄 Course réattribuée")
                            st.rerun()
                with col4:
                    if st.button(f"🗑️ Supprimer", key=f"delete_{course['id']}"):
                        st.session_state.courses = [c for c in st.session_state.courses if c['id'] != course['id']]
                        st.success("🗑️ Course supprimée")
                        st.rerun()
            
            # Badge propriétaire
            if course['depose_par'] == user['email']:
                with col5:
                    st.markdown("""
                    <span style="background: #eff6ff; color: #2563eb; padding: 8px 16px; 
                                 border-radius: 10px; font-size: 0.85rem; font-weight: 500;">
                        📌 Ma course déposée
                    </span>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

# ============ MAIN ============
def main():
    if not st.session_state.logged_in:
        show_login()
    else:
        show_app()

if __name__ == "__main__":
    main()
