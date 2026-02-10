# app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import random
from geopy.distance import geodesic  # do liczenia odległości między punktami

st.title("Quiz geograficzny 🌍")
st.set_page_config(layout="wide", initial_sidebar_state="auto")

# Słownik obiektów (przykład, możesz wstawić całą swoją listę)
# Tworzymy słownik obiektów z przykładowymi współrzędnymi
# Klucz: nazwa obiektu, wartość: [szerokość, długość]
objects = {
    # --- MORZA I ZATOKI ---
    "Morze Karskie": [74.8, 77.1],
    "Morze Łaptiewów": [75.4, 125.8],
    "Morze Czukockie": [69.6, -171.4],
    "Morze Ochockie": [54.3, 148.7],
    "Morze Japońskie": [39.5, 134.5],
    "Morze Żółte": [35.0, 123.0],
    "Morze Południowochińskie": [12.1, 113.3],
    "Morze Arabskie": [15.8, 65.2],
    "Zatoka Perska": [26.9, 51.5],
    "Zatoka Omańska": [24.4, 58.5],
    "Zatoka Bengalska": [14.7, 88.3],
    "Zatoka Tajlandzka": [10.2, 101.3],
    "Morze Czerwone": [22.0, 38.0],
    "Zatoka Gwinejska": [2.0, 6.0],
    "Morze Beringa": [58.4, -174.4],
    "Morze Beauforta": [73.5, -139.1],
    "Zatoka Hudsona": [60.0, -85.0],
    "Zatoka Meksykańska": [25.3, -90.3],
    "Zatoka Kalifornijska": [26.0, -110.0],
    "Morze Koralowe": [-18.0, 155.0],
    "Morze Tasmana": [-37.0, 160.0],
    "Wielka Zatoka Australijska": [-33.0, 130.0],

    # --- CIEŚNINY ---
    "Cieśnina Koreańska": [34.5, 129.5],
    "Cieśnina Malakka": [2.5, 102.1],
    "Cieśnina Ormuz": [26.5, 56.2],
    "Cieśnina Bab-al-Mandab": [12.5, 43.3],
    "Kanał Mozambicki": [-18.0, 41.0],
    "Cieśnina Beringa": [66.0, -169.0],
    "Cieśnina Davisa": [67.0, -58.0],
    "Cieśnina Magellana": [-53.1, -70.9],
    "Cieśnina Gibraltarska": [35.9, -5.4],
    "Cieśnina Bass": [-39.9, 146.1],
    "Cieśnina Cooka": [-41.2, 174.4],
    "Cieśnina Torresa": [-9.8, 142.5],

    # --- PÓŁWYSPY ---
    "Półwysep Arabski": [23.8, 45.0],
    "Indochiny": [15.0, 102.0],
    "Indyjski": [19.0, 78.0],
    "Kamczatka": [56.0, 160.0],
    "Półwysep Somalijski": [9.0, 48.0],
    "Labrador": [55.0, -68.0],
    "Floryda": [28.1, -81.6],
    "Jukatan": [19.3, -89.1],
    "Półwysep Jork": [-12.2, 142.6],

    # --- WYSPY ---
    "Nowa Ziemia": [74.5, 56.0],
    "Sachalin": [50.5, 142.7],
    "Hokkaido": [43.2, 142.3],
    "Honsiu": [36.2, 138.2],
    "Tajwan": [23.6, 120.9],
    "Borneo": [1.0, 114.0],
    "Sumatra": [-0.5, 101.3],
    "Madagaskar": [-18.7, 46.8],
    "Kanaryjskie": [28.2, -15.9],
    "Grenlandia": [72.0, -40.0],
    "Kuba": [21.5, -77.7],
    "Ziemia Ognista": [-54.0, -69.0],
    "Falklandy": [-51.7, -59.1],
    "Nowa Gwinea": [-5.4, 141.2],
    "Tasmania": [-42.0, 147.3],
    "Nowa Zelandia": [-40.9, 174.8],

    # --- NIZINY, KOTLINY I PUSTYNIE ---
    "Nizina Zachodniosyberyjska": [62.0, 75.0],
    "Nizina Chińska": [34.0, 116.0],
    "Mezopotamia": [33.0, 44.0],
    "Pustynia Gobi": [42.5, 103.4],
    "Rub-al-Chali": [20.0, 50.0],
    "Kotlina Konga": [-1.0, 22.0],
    "Sahara": [23.0, 13.0],
    "Pustynia Kalahari": [-23.0, 22.0],
    "Nizina Amazonki": [-3.0, -60.0],
    "Wielka Kotlina": [39.0, -118.0],
    "Atakama": [-24.5, -69.2],
    "Wielka Pustynia Wiktorii": [-28.5, 128.5],

    # --- PASMA GÓRSKIE ---
    "Himalaje": [27.9, 86.9],
    "Ural": [60.0, 60.0],
    "Tienszan": [42.0, 80.0],
    "Ałtaj": [49.0, 89.0],
    "Kaukaz": [42.6, 44.5],
    "Atlas": [31.6, -5.1],
    "Góry Smocze": [-29.0, 29.0],
    "Andy": [-32.6, -70.0],
    "Kordyliery": [45.0, -120.0],
    "Appalachy": [37.0, -80.0],
    "Wielkie Góry Wododziałowe": [-25.0, 147.0],
    "Alpy Południowe": [-43.4, 170.4],

    # --- RZEKI ---
    "Ob": [66.7, 66.5],
    "Jenisej": [71.8, 82.6],
    "Lena": [72.4, 126.7],
    "Amur": [52.9, 140.6],
    "Jangcy": [31.2, 121.4],
    "Ganges": [25.3, 83.0],
    "Eufrat": [31.0, 47.4],
    "Nil": [30.1, 31.1],
    "Kongo": [-6.0, 12.4],
    "Niger": [13.5, 2.0],
    "Amazonka": [-0.1, -49.1],
    "Missisipi": [29.1, -89.2],
    "Mackenzie": [68.9, -134.8],
    "Murray": [-35.3, 139.3],

    # --- JEZIORA ---
    "Bajkał": [53.5, 108.1],
    "Morze Kaspijskie": [41.6, 50.6],
    "Aral": [45.0, 59.0],
    "Jezioro Wiktorii": [-1.0, 33.0],
    "Tanganika": [-6.4, 29.6],
    "Niasa": [-12.1, 34.5],
    "Jezioro Górne": [47.7, -87.5],
    "Michigan": [44.0, -87.0],
    "Huron": [45.0, -82.0],
    "Erie": [42.2, -81.2],
    "Ontario": [43.6, -77.9],
    "Titicaca": [-15.7, -69.4],
    "Eyre": [-28.4, 137.3],
    
    # EUROPA
    # --- MORZA I ZATOKI ---
    "Morze Bałtyckie": [58.5, 20.0],
    "Morze Północne": [56.0, 3.0],
    "Morze Śródziemne": [35.0, 18.0],
    "Morze Norweskie": [69.0, 2.0],
    "Morze Czarne": [43.4, 34.5],
    "Morze Adriatyckie": [43.0, 15.0],
    "Morze Egejskie": [38.5, 25.5],
    "Zatoka Biskajska": [45.5, -3.5],
    "Zatoka Botnicka": [62.0, 19.5],

    # --- CIEŚNINY ---
    "Cieśnina Gibraltarska": [35.9, -5.4],
    "Kanał La Manche": [50.0, -2.0],
    "Bosfor": [41.1, 29.1],
    "Dardanele": [40.2, 26.4],
    "Skagerrak": [57.8, 9.0],

    # --- PÓŁWYSPY ---
    "Półwysep Skandynawski": [63.0, 14.0],
    "Półwysep Iberyjski": [40.0, -4.0],
    "Półwysep Apeniński": [42.0, 14.0],
    "Półwysep Bałkański": [42.0, 22.0],
    "Półwysep Jutlandzki": [55.5, 9.2],
    "Półwysep Krymski": [45.2, 34.2],

    # --- WYSPY ---
    "Wielka Brytania": [54.0, -2.0],
    "Islandia": [64.9, -18.5],
    "Irlandia": [53.2, -8.0],
    "Sycylia": [37.6, 14.0],
    "Sardynia": [40.1, 9.0],
    "Korsyka": [42.1, 9.1],
    "Kreta": [35.2, 24.8],

    # --- GÓRY ---
    "Alpy": [46.5, 10.0],
    "Karpaty": [47.0, 25.5],
    "Pireneje": [42.6, 1.0],
    "Apeniny": [43.0, 13.5],
    "Góry Skandynawskie": [63.0, 10.0],
    "Góry Dynarskie": [43.0, 18.5],

    # --- RZEKI ---
    "Wołga": [48.0, 46.0],
    "Dunaj": [45.2, 29.7],
    "Ren": [50.0, 8.0],
    "Wisła": [52.0, 19.0],
    "Łaba": [52.0, 12.0],
    "Tag": [39.5, -4.0],
    "Loara": [47.3, 0.7],
    "Tamiza": [51.5, 0.0],
    "Dniepr": [47.0, 33.0],

    # --- JEZIORA ---
    "Ładoga": [60.1, 31.2],
    "Onega": [61.7, 35.4],
    "Wener": [58.8, 13.2],
    "Jezioro Genewskie": [46.4, 6.5],
    "Balaton": [46.8, 17.7],
    "Bodeńskie": [47.6, 9.4],

    # --- NIZINY I KRAINY ---
    "Nizina Wschodnioeuropejska": [55.0, 35.0],
    "Nizina Niemiecka": [52.5, 10.0],
    "Nizina Francuska": [47.0, 0.0],
    "Nizina Padańska": [45.0, 10.0],
    "Nizina Panońska": [46.5, 19.5]
}


# Parametr, ile km od prawidłowego miejsca uznajemy za poprawny klik
ACCEPTABLE_DISTANCE_KM = 200  

# Inicjalizacja sesji
if "current_object" not in st.session_state:
    st.session_state.current_object = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "found_objects" not in st.session_state:
    st.session_state.found_objects = {}

st.session_state.hint_used = False


if st.button("Podpowiedź"):
    st.session_state.hint_used = True


# Losujemy nowy obiekt, jeśli nie ma aktualnego
if st.session_state.current_object is None:
    remaining = [obj for obj in objects if obj not in st.session_state.found_objects]
    if remaining:
        st.session_state.current_object = random.choice(remaining)
    else:
        st.write("Gratulacje! Ukończyłeś wszystkie obiekty!")
        st.stop()

st.write(f"Znajdź na mapie: *{st.session_state.current_object}*")

# Tworzymy mapę
m = folium.Map(location=[20, 0], zoom_start=2)

# Wyświetlamy już odkryte obiekty
for name, coords in st.session_state.found_objects.items():
    folium.Marker(location=coords, popup=f"{name} ✅").add_to(m)

# Wyświetlamy podpowiedź, jeśli użyto przycisku
if st.session_state.hint_used:
    hint_coords = objects[st.session_state.current_object]
    folium.Marker(
        location=hint_coords,
        popup=f"Podpowiedź: {st.session_state.current_object}",
        icon=folium.Icon(color="orange", icon="info-sign")
    ).add_to(m)

# Obsługa kliknięcia
map_data = st_folium(m, width=1000, height=700, returned_objects=["last_clicked"])

if map_data["last_clicked"]:
    click_lat = map_data["last_clicked"]["lat"]
    click_lon = map_data["last_clicked"]["lng"]
    correct_coords = objects[st.session_state.current_object]
    distance = geodesic((click_lat, click_lon), correct_coords).km

    if distance <= ACCEPTABLE_DISTANCE_KM:
        st.success(f"Poprawnie! {st.session_state.current_object} znajduje się tutaj ✅")
        st.session_state.found_objects[st.session_state.current_object] = correct_coords
        st.session_state.score += 1
        st.session_state.current_object = None  # przygotowanie do następnego obiektu
    else:
        st.error(f"Niepoprawnie! Spróbuj ponownie. Twój błąd: {int(distance)} km")

st.write(f"Twój wynik: {st.session_state.score} / {len(objects)}")