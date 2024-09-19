# import joblib
import pandas as pd
from django.conf import settings
from typing import Any, Text, Dict, List
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
import re
import requests
import sys
import os
import django
from asgiref.sync import sync_to_async


# actions.py
# Define a mapping of synonyms to the main term, including common mistakes
MAPPING = {
    'itching': ['pruritus', 'skin irritation', 'itching sensation', 'itiching', 'itchng', 'pruitus', 'puritus','ichting'],
    'skin_rash': ['rash', 'dermatitis', 'hives', 'skin rash', 'skin rashes', 'sking rash', 'skin-rash', 'rashs'],
    'nodal_skin_eruptions': ['nodules', 'lumps', 'skin bumps', 'nodal skin eruptions', 'nodal skin eruption', 'nodal_sking_eruptions', 'nodal_skin_eruptin', 'skin_eruptions'],
    'dischromic_patches': ['skin discoloration', 'pigment changes', 'hypo/hyperpigmentation', 'dischromic patches', 'dischromic patch', 'dyschromic_patches', 'discolor_patches', 'dyschromic_patches', 'dischromic_patchs'],
    'continuous_sneezing': ['sneezing fits', 'repeated sneezing', 'persistent sneezing', 'continuous sneezing', 'continuous sneeze', 'continous_sneezing', 'continuos_sneezing', 'sneezing_fits', 'repeated_sneezing'],
    'shivering': ['chills', 'trembling', 'shaking', 'shivering', 'shiver', 'shiverring', 'shivvering', 'shiverng', 'chils'],
    'chills': ['cold sensation', 'shivers', 'rigors', 'chills', 'chill', 'chils', 'chillz', 'shivvers', 'rigors'],
    'watering_from_eyes': ['teary eyes', 'lacrimation', 'watery eyes', 'watering from eyes', 'water from eyes', 'wattering_from_eyes', 'watering_eyes', 'tear_eyes', 'lacrimations'],
    'stomach_pain': ['abdominal pain', 'tummy ache', 'stomach ache', 'stomach pain', 'stomach pains', 'stomaach_pain', 'abdonimal_pain', 'tummyy_ache', 'stomaach_pains'],
    'acidity': ['heartburn', 'acid reflux', 'sour stomach', 'acidity', 'acity', 'acid_reflux', 'sour_stomach', 'acidiity'],
    'ulcers_on_tongue': ['tongue sores', 'canker sores', 'mouth ulcers', 'ulcers on tongue', 'tongue ulcers', 'ulces_on_tongue', 'ulers_on_tongue', 'canker_sore', 'tounge_ulcers'],
    'vomiting': ['emesis', 'throwing up', 'nausea with vomiting', 'vomiting', 'vomit', 'vomitting', 'vommiting', 'emesis', 'thrwoing_up'],
    'cough': ['hacking', 'throat clearing', 'persistent cough', 'cough', 'coughing', 'coug', 'caugh', 'coughin', 'hacking'],
    'chest_pain': ['thoracic pain', 'chest discomfort', 'angina', 'chest pain', 'chest pains', 'ches_pain', 'thoractic_pain', 'chest_discomfort', 'angina'],
    'yellowish_skin': ['jaundice', 'yellowing of the skin', 'yellow complexion', 'yellowish skin', 'yellowsh_skin', 'yelloish_skin', 'jaundic', 'yellowing_skin'],
    'nausea': ['queasiness', 'urge to vomit', 'sick feeling', 'nausea', 'nausaea', 'nauzea', 'queasiness', 'sick_feeling'],
    'loss_of_appetite': ['anorexia', 'decreased hunger', 'lack of appetite', 'loss of appetite', 'lose_of_appetite', 'appetite_loss', 'lack_of_appetite', 'anorexia'],
    'abdominal_pain': ['belly pain', 'gut pain', 'stomach cramps', 'abdominal pain', 'abdomnial_pain', 'belly_pain', 'gut_pain', 'stomch_cramps'],
    'yellowing_of_eyes': ['jaundice', 'scleral icterus', 'yellow sclera', 'yellowing of eyes', 'yellow_of_eyes', 'scleral_icterus', 'jaundiced_eyes', 'yellowing_eyes'],
    'burning_micturition': ['painful urination', 'dysuria', 'burning sensation while urinating', 'burning micturition', 'burning_urination', 'dysuria', 'painful_urination', 'burning_micturition'],
    'spotting_urination': ['urinary spotting', 'spotting after urination', 'blood spots in urine', 'spotting urination', 'spotting_urin', 'urinary_spottng', 'blood_spots_in_urine', 'urinary_spottng'],
    'passage_of_gases': ['flatulence', 'passing gas', 'farting', 'passage of gases', 'gas_passing', 'passage_of_gas', 'flatulance', 'farting'],
    'internal_itching': ['internal pruritus', 'deep itching', 'itching sensation inside', 'internal itching', 'internal_pruitus', 'deep_itching', 'internal_itiching', 'itching_sensation_inside'],
    'indigestion': ['dyspepsia', 'upset stomach', 'stomach discomfort', 'indigestion', 'indigestion', 'dyspepsa', 'stomach_discomfort', 'dyspepsia'],
    'muscle_wasting': ['muscle atrophy', 'muscle loss', 'muscle degradation', 'muscle wasting', 'muscle_atrophy', 'muscle_wasting', 'muscle_loss', 'muscle_degradation'],
    'patches_in_throat': ['throat patches', 'white patches', 'throat spots', 'patches in throat', 'patchs_in_throat', 'white_patchs', 'throat_paches', 'throat_spots'],
    'high_fever': ['hyperpyrexia', 'elevated temperature', 'severe fever','fever', 'high fever', 'high_fever', 'hyperpyrexia', 'elevated_temperature', 'severe_fever'],
    'extra_marital_contacts': ['infidelity', 'extramarital affairs', 'adultery', 'extra marital contacts', 'extra_marital_affairs', 'extramartial_contacts', 'adultery', 'marital_affairs'],
    'fatigue': ['tiredness', 'exhaustion', 'weariness', 'fatigue', 'fatigued', 'tiredeness', 'exaustion', 'weariness'],
    'weight_loss': ['slimming', 'reduction in weight', 'unintentional weight loss', 'weight loss', 'weight_loos', 'reduction_in_weight', 'slimming', 'weight_loss'],
    'restlessness': ['agitation', 'inability to rest', 'unease', 'restlessness', 'restlesness', 'agitation', 'unease', 'inability_to_rest'],
    'lethargy': ['sluggishness', 'fatigue', 'lack of energy', 'lethargy', 'letharg', 'sluggishness', 'lack_of_energy', 'fatigue'],
    'irregular_sugar_level': ['fluctuating blood sugar', 'unstable glucose levels', 'erratic blood sugar', 'irregular sugar level', 'irregular_sugar_levels', 'fluctuating_sugar', 'erratic_sugar', 'unstable_glucose'],
    'blurred_and_distorted_vision': ['hazy vision', 'unclear sight', 'vision impairment', 'blurred and distorted vision', 'blurred_vision', 'hazy_vision', 'distorted_sight', 'vision_impairment'],
    'obesity': ['overweight', 'excessive weight', 'high body mass', 'obesity', 'obesisty', 'overweight', 'excessive_weight', 'high_body_mass'],
    'excessive_hunger': ['polyphagia', 'extreme appetite', 'uncontrollable hunger', 'excessive hunger', 'excess_hunger', 'uncontrollable_appetite', 'polyphagia', 'extreme_appetite'],
    'increased_appetite': ['hyperphagia', 'enhanced appetite', 'greater hunger', 'increased appetite', 'increased_appetitte', 'hyperphagia', 'enhanced_hunger', 'greater_appetite'],
    'polyuria': ['excessive urination', 'frequent urination', 'high urine output', 'polyuria', 'polyuria', 'frequent_urin', 'high_urine_output', 'excessive_urination'],
    'sunken_eyes': ['hollow eyes', 'deep-set eyes', 'sunken eye sockets', 'sunken eyes', 'sunkne_eyes', 'deep_set_eyes', 'hollow_eyes', 'sunken_eye_socktes'],
    'dehydration': ['lack of hydration', 'body water deficiency', 'fluid depletion', 'dehydration', 'dehydrattion', 'fluid_deficiency', 'lack_of_hydration', 'dehydration'],
    'diarrhoea': ['loose stools', 'watery stools', 'frequent bowel movements', 'diarrhoea', 'diarrhea', 'loose_stols', 'frequent_bowel_movement', 'watery_stools'],
    'breathlessness': ['shortness of breath', 'dyspnea', 'difficulty breathing', 'breathlessness', 'breathlessnesss', 'shortness_of_breath', 'difficulty_breathing', 'dyspnea'],
    'family_history': ['hereditary conditions', 'genetic history', 'familial background', 'family history', 'familly_history', 'hereditary_conditions', 'genetic_background', 'familial_background'],
    'mucoid_sputum': ['mucus cough', 'phlegm', 'slimy sputum', 'mucoid sputum', 'mucous_sputum', 'phlem', 'slimmy_sputum', 'mucoid_sputm'],
    'headache': ['cephalalgia', 'head pain', 'migraine', 'headache', 'headeache', 'cephalgia', 'headpains', 'migrain'],
    'dizziness': ['lightheadedness', 'vertigo', 'unsteadiness', 'dizziness', 'dizzyness', 'lightheadness', 'vertigo', 'unsteady'],
    'loss_of_balance': ['imbalance', 'unsteady gait', 'difficulty standing', 'loss of balance', 'lose_of_balance', 'imbalance', 'unsteady_gait', 'difficulty_standing'],
    'lack_of_concentration': ['poor focus', 'inattentiveness', 'distractedness', 'lack of concentration', 'lack_of_concentrtion', 'poor_focus', 'inattentivness', 'distractedness'],
    'stiff_neck': ['neck rigidity', 'neck stiffness', 'tight neck', 'stiff neck', 'stif_neck', 'neck_rigidity', 'tight_nack', 'neck_stiffness'],
    'depression': ['low mood', 'clinical depression', 'major depressive disorder', 'depression', 'depresssion', 'low_mood', 'clinical_depression', 'major_depressive_disorder'],
    'irritability': ['short temper', 'grumpiness', 'agitation', 'irritability', 'irritable', 'grumpyness', 'short_temper', 'agitaton'],
    'visual_disturbances': ['vision problems', 'eye disturbances', 'visual issues', 'visual disturbances', 'visual_dissurbances', 'vision_issues', 'eye_disturbances', 'visual_disturbance'],
    'back_pain': ['lumbar pain', 'spine ache', 'dorsal discomfort', 'back pain', 'backpains', 'lumbar_pain', 'spine_discomfort', 'dorsal_pain'],
    'weakness_in_limbs': ['limb fatigue', 'weak arms/legs', 'muscle weakness', 'weakness in limbs', 'weakness_in_limbs', 'limb_fatigue', 'weak_limbs', 'muscle_fatigue'],
    'neck_pain': ['cervical pain', 'neck discomfort', 'neck ache', 'neck pain', 'neckpains', 'cervical_pain', 'neck_discomfort', 'neck_ache'],
    'weakness_of_one_body_side': ['hemiparesis', 'one-sided weakness', 'partial paralysis', 'weakness of one body side', 'hemiparesis', 'one_side_weakness', 'partial_paralysis', 'weakness_of_one_side'],
    'altered_sensorium': ['confused state', 'altered consciousness', 'disoriented', 'altered sensorium', 'altered_sensirium', 'confused_state', 'altered_consciousness', 'disoriented'],
    'dark_urine': ['concentrated urine', 'deep-colored urine', 'brownish urine', 'dark urine', 'dark_urine', 'concentrated_urine', 'deep_colored_urine', 'brownish_urine'],
    'sweating': ['perspiration', 'excessive sweating', 'diaphoresis', 'sweating', 'sweaating', 'perspiration', 'excessive_sweating', 'diaphoresis'],
    'muscle_pain': ['myalgia', 'muscle ache', 'sore muscles', 'muscle pain', 'muscle_pains', 'myagia', 'muscle_ache', 'sore_muscles'],
    'mild_fever': ['low-grade fever', 'slight fever', 'mild temperature', 'mild fever','fever', 'mild_fever', 'low_grade_fever', 'slight_fever', 'mild_temperatuer'],
    'swelled_lymph_nodes': ['swollen glands', 'lymphadenopathy', 'enlarged lymph nodes', 'swelled lymph nodes', 'swelled_lymph_nodes', 'swollen_glands', 'lymphadenopathy', 'enlarged_lymph_nodes'],
    'malaise': ['general discomfort', 'feeling unwell', 'unease', 'malaise', 'malaise', 'general_discomfort', 'feeling_unwell', 'unease'],
    'red_spots_over_body': ['rash', 'petechiae', 'red blotches', 'red spots over body', 'rash', 'petechiae', 'red_blotches', 'red_spots_over_body'],
    'joint_pain': ['arthralgia', 'joint ache', 'sore joints', 'joint pain', 'arthralgia', 'joint_ache', 'sore_joints', 'joint_pains'],
    'pain_behind_the_eyes': ['ocular pain', 'retro-orbital pain', 'eye socket pain', 'pain behind the eyes', 'ocular_pain', 'retro_orbital_pain', 'eye_socket_pain', 'pain_behind_eyes'],
    'constipation': ['hard stools', 'bowel irregularity', 'difficulty passing stools', 'constipation', 'constipation', 'hard_stools', 'bowel_irregularity', 'difficulty_passing_stools'],
    'toxic_look': ['ill appearance', 'sickly look', 'unwell appearance', 'toxic look', 'toxic_look', 'ill_appearance', 'sickly_look', 'unwell_appearance'],
    'belly_pain': ['abdominal pain', 'stomach cramps', 'gut ache', 'belly pain', 'belly_pain', 'abdominal_pain', 'stomach_cramps', 'gut_ache'],
    'cramps': ['muscle spasms', 'cramps', 'cramping', 'cramps', 'crampss', 'cramp', 'musclee spasmss', 'crampings'],
    'bruising': ['contusions', 'ecchymosis', 'black-and-blue marks', 'bruising', 'bruizing', 'brusing', 'contusion', 'bruiseing'],
    'swelling_of_stomach': ['bloating', 'abdominal swelling', 'distended stomach', 'swelling of stomach', 'swelling_of_stomack', 'abdominal_swellingg', 'distended_stomak', 'bloatingg'],
    'swollen_legs': ['leg edema', 'fluid retention in legs', 'leg swelling', 'swollen legs', 'swolen_legs', 'swollen_leggs', 'flud_retention', 'leg_sweling'],
    'black_stools': ['melena', 'tarry stools', 'dark bowel movements', 'black stools', 'black_stool', 'melanna', 'dark_bowels', 'tarry_stool'],
    'watery_diarrhoea': ['watery stools', 'loose motions', 'liquid diarrhea', 'watery diarrhoea', 'watery_diarrhoea', 'loose_motionss', 'liquid_diarrhoea', 'watery_diarrhea'],
    'swelled_blood_vessels': ['varicose veins', 'engorged blood vessels', 'enlarged veins', 'swelled blood vessels', 'swolen_blood_vessels', 'varicose_veins', 'engorged_blood_vessel', 'swelled_blood_vessel'],
    'prominent_veins_on_calf': ['visible calf veins', 'calf varicose veins', 'bulging veins', 'prominent veins on calf', 'prominant_veins_on_calf', 'visibile_calf_veins', 'calf_varicose_vein', 'bulging_vein'],
    'weight_gain': ['increase in weight', 'weight increase', 'gaining weight', 'weight gain', 'weight_gainn', 'increase_weight', 'gain_weight', 'weight_gain'],
    'puffy_face_and_eyes': ['facial swelling', 'swollen face and eyes', 'puffiness', 'puffy face and eyes', 'pufffy_face_and_eyes', 'facial_sweling', 'swolen_face', 'puffy_face_and_eyes'],
    'cold_hands_and_feets': ['chilly extremities', 'cold hands and feet', 'cold limbs', 'cold hands and feets', 'cold_hands_and_feet', 'chilly_extremeties', 'cold_limbs', 'cold_hands_and_feets'],
    'mood_swings': ['emotional instability', 'mood changes', 'mood fluctuations', 'mood swings', 'mood_swingss', 'emotionnal_instability', 'mood_change', 'mood_swing'],
    'hip_joint_pain': ['hip pain', 'hip discomfort', 'pain in hip joint', 'hip joint pain', 'hip_joint_painn', 'hip_disscomfort', 'pain_in_hip_joint', 'hip_joint_pain'],
    'movement_stiffness': ['rigidity', 'stiffness in movement', 'difficulty moving', 'movement stiffness', 'movement_stifness', 'rigity', 'stifness_in_movement', 'difficulty_movinng'],
    'pain_in_anal_region': ['rectal pain', 'anal discomfort', 'pain in anus', 'pain in anal region', 'pain_in_anal_regoin', 'rectal_disscomfort', 'pain_in_anus', 'anal_region_pain'],
    'bloody_stool': ['hematochezia', 'blood in stool', 'red stools', 'bloody stool', 'bloody_stools', 'hemorrrhage', 'blood_in_stool', 'red_stool'],
    'irritation_in_anus': ['anal itching', 'irritation of anus', 'anal discomfort', 'irritation in anus', 'irritaion_in_anus', 'anal_itching', 'irritation_of_anus', 'anal_disscomfort'],
    'neck_stiffness': ['stiff neck', 'neck rigidity', 'tight neck', 'neck stiffness', 'neck_stifness', 'stiff_neck', 'neck_rigidity', 'tight_neck'],
    'mucus_in_stool': ['mucoid stools', 'mucus discharge in stool', 'slimy stool', 'mucus in stool', 'mucous_in_stool', 'mucoid_stools', 'slimy_stools', 'mucus_in_stoll'],
    'knee_pain': ['patellar pain', 'knee ache', 'discomfort in knee', 'knee pain', 'knee_pains', 'patellor_pain', 'knee_achee', 'discomfort_in_knee'],
    'hip_pain': ['hip ache', 'discomfort in hip', 'pain in hip', 'hip pain', 'hip_pains', 'hip_discomfort', 'pain_in_hip', 'hip_pain'],
    'swelling_joints': ['joint edema', 'swollen joints', 'enlarged joints', 'swelling joints', 'swollen_joints', 'joint_edema', 'enlargged_joints', 'swelling_joint'],
    'painful_walking': ['difficulty walking', 'pain during walking', 'walking discomfort', 'painful walking', 'painful_waliking', 'difficulty_walk', 'pain_during_walking', 'walking_disscomfort'],
    'small_dents_in_nails': ['nail pitting', 'dents in nails', 'nail surface irregularities', 'small dents in nails', 'small_dent_in_nails', 'nail_piting', 'dent_in_nails', 'nail_surface_irrregularities'],
    'brittle_nails': ['weak nails', 'fragile nails', 'easily breakable nails', 'brittle nails', 'brittle_nailss', 'weak_nail', 'fragile_nail', 'easily_breakable_nail'],
    'swollen_extremeties': ['extremity edema', 'swollen arms/legs', 'swollen hands/feet', 'swollen extremities', 'swollen_extremeties', 'extremity_edema', 'swollen_extremeties', 'swollen_arm_legs'],
    'sunken_cheeks': ['hollow cheeks', 'cheek indentation', 'gaunt face', 'sunken cheeks', 'sunked_cheeks', 'hollow_cheeks', 'cheek_indentation', 'gaunt_face'],
    'scarring': ['scar tissue', 'scar formation', 'marks after injury', 'scarring', 'scarrinng', 'scar_tissue', 'scaring', 'marks_after_injury'],
    'blister': ['skin blister', 'fluid-filled blister', 'raised blister', 'blister', 'blisters', 'skin_bllister', 'fluid_filled_bllister', 'raised_bllister'],
    'skin_peeling': ['desquamation', 'peeling skin', 'flaking skin', 'skin peeling', 'skin_peelinng', 'desquamationn', 'peeling_skin', 'flaking_skin'],
    'silver_like_dusting': ['silvery scales', 'scaly skin', 'silver dusting on skin', 'silver like dusting', 'silver_like_dustng', 'silvery_scale', 'scaly_skin', 'silver_dusting_on_skin'],
    'small_blisters_on_skin': ['vesicles', 'skin blisters', 'tiny skin blisters', 'small blisters on skin', 'small_blisters_on_skin', 'vesicales', 'tiny_skin_bllisters', 'small_blister_on_skin'],
    'red_sore_around_nose': ['nasal sores', 'red sores on nose', 'inflamed area around nose', 'red sore around nose', 'red_sore_around_nose', 'nasal_sore', 'inflamed_area_around_nose', 'red_sores_on_nose'],
    'yellow_crust_ooze': ['crusty yellow discharge', 'oozing sores', 'yellow crusted areas', 'yellow crust ooze', 'yellow_crust_ooze', 'crusty_yellow_discharge', 'oozing_sore', 'yellow_crusted_area']
}


# Add the parent directory of 'vdocBackend' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vdocBackend.settings')

# Initialize Django
django.setup()

print(os.getcwd())
print(os.listdir(os.getcwd()))

from app.models import Diseases, Description, Diet , Precaution , Medication

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import re

def get_diseases(symptoms_list) :
    
    data1 = pd.read_csv('actions/Diseases1.csv')

    # Get unique values from the selected columns
    unique_values = pd.unique(data1.drop(labels='Disease',axis=1).values.ravel())

    # Convert to a list if needed
    unique_values_list = unique_values.tolist()
    data = pd.get_dummies(data1.drop(labels='Disease',axis=1))
    data['Disease'] = data1['Disease']
    le = LabelEncoder()
    data['Disease'] = le.fit_transform(data['Disease'])
    x = data.drop(columns=['Disease', 'Diseases_id', 'Description_id', 'Precaution_id', 'Medication_id', 'Diet_id', 'Diseases_severity'])
    y = pd.DataFrame(data['Disease'])
    x_train , x_test , y_train , y_test = train_test_split(x,y,random_state=20,test_size=0.2)
    rf = RandomForestClassifier(n_estimators=100)
    multi_target_rf = MultiOutputClassifier(rf, n_jobs=-1)
    multi_target_rf.fit(x_train,y_train)

    c = []
    columns_name = x.columns
    for i in columns_name :
        c.append(re.split(r'Symptom_\d+_', i)[1].strip())
    l = symptoms_list
    print(list(l))
    new = {}
    for i in range(len(columns_name)) :
        if c[i] in l :
            new[columns_name[i]] = 1 
        else :
            new[columns_name[i]] = 0

    sp = multi_target_rf.predict(pd.DataFrame([new]))
    predicted_label = le.inverse_transform(sp.reshape(-1))[0]
    return predicted_label if predicted_label else None


@sync_to_async
def get_disease_details(predicted_label):
    disease_obj = Diseases.objects.filter(Disease=predicted_label).first()
    if disease_obj:
        description = disease_obj.Description_id.Disease_description
        print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n\n')
        print(disease_obj)
        print('\n\njjjjjjjjjjjjjjjjjjjjj')
        # description = disease_obj.Disease_description
        # description = Description.objects.get(Disease=disease_obj).Disease_description
        print(f'\n\n\n\n\n\n{description}\n\n\n\n\n')
        details = {
            "disease": disease_obj.Disease,
            "severity": disease_obj.Disease_severity,
            "description": description,
        }
        return details
    return None

class ActionRetrieveDiseases(Action):
    def name(self) -> Text:
        return "action_retrieve_diseases"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: DomainDict) -> List[Dict[Text, Any]]:
        # Retrieve symptoms from the slot
        symptoms = tracker.get_latest_entity_values('symptom')

        if not symptoms:
            dispatcher.utter_message(text="No symptoms provided.")
            return []

        else :
            normalized_symptoms = []
            for symptom in symptoms:
                normalized = None
                # Check if the symptom matches any common mistakes
                for main_term, mistakes in MAPPING.items():
                    if symptom in mistakes:
                        normalized = main_term
                        break
                # If no match found, default to the symptom itself
                if not normalized:
                    normalized = symptom
                normalized_symptoms.append(normalized)
            # print(symptoms)

            # Predict diseases
            predicted_label = get_diseases(normalized_symptoms)
            print('\n\n\n\n\n\n\n\n\n\n')
            print(predicted_label)
            print('\n\n\n\n\n\n\n\n\n\n')

            if predicted_label:
                print('in1')
                details = await get_disease_details(predicted_label)
                print('in1.1')
                if details:
                    print('in2')
                    response = f"Disease: {details['disease']}\n Severity: {details['severity']}\n Description: {details['description']}"
                    dispatcher.utter_message(text=response)
                    return [SlotSet("diseases", details['disease'])]
            else:
                dispatcher.utter_message(text="No diseases found based on the provided symptoms.")
                return [SlotSet("diseases", '')]


from asgiref.sync import sync_to_async

@sync_to_async      
def get_precaution(diseases_name):
    precaution_obj = Precaution.objects.filter(Disease=diseases_name).first()
    if precaution_obj:
        return [precaution_obj.Precaution_1, precaution_obj.Precaution_2, 
                precaution_obj.Precaution_3, precaution_obj.Precaution_4]
    return None

class StatePrecaution(Action):
    def name(self) -> Text:
        return "state_precaution"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        # Get the predicted disease from the slot
        diseases_name = tracker.get_slot('diseases')

        if not diseases_name:
            dispatcher.utter_message(text="I couldn't find any diseases to provide precautions for.")
            return []

        # Fetch the precautions for the predicted disease (async)
        predicted_label = await get_precaution(diseases_name)

        if predicted_label:
            # Prepare the message with precautions
            prediction = ''
            for c, precaution in enumerate(predicted_label, 1):
                if precaution:  # Only include non-None precautions
                    prediction += f'Precaution {c}: {precaution}\n'
            
            dispatcher.utter_message(text=f"I'll provide you with some precautions:\n\n{prediction}")
        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find any precautions for the disease.")

        return []


@sync_to_async      
def get_medication(diseases_name):
    medication_obj = Medication.objects.filter(Disease=diseases_name).first()
    if medication_obj:
        return (list(medication_obj.Disease_medication))
    return None

class StateMedication(Action):
    def name(self) -> Text:
        return "state_medication"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        # Get the predicted disease from the slot
        diseases_name = tracker.get_slot('diseases')

        if not diseases_name:
            dispatcher.utter_message(text="I couldn't find any diseases to provide medication for.")
            return []

        # Fetch the precautions for the predicted disease (async)
        predicted_label = await get_medication(diseases_name)

        if predicted_label:
            # Prepare the message with precautions
            prediction = ''
            for c, medication in enumerate(predicted_label, 1):
                if medication:  # Only include non-None precautions
                    prediction += f'Medication {c}: {medication}\n'
            
            dispatcher.utter_message(text=f"I'll provide you with some medications:\n\n{medication}")
        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find any medications for the disease.")

        return []



@sync_to_async      
def get_diet(diseases_name):
    diet_obj = Diet.objects.filter(Disease=diseases_name).first()
    if diet_obj:
        return (list(diet_obj.Disease_Diet))
    return None

class StateDiet(Action):
    def name(self) -> Text:
        return "state_diet"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        # Get the predicted disease from the slot
        diseases_name = tracker.get_slot('diseases')

        if not diseases_name:
            dispatcher.utter_message(text="I couldn't find any diseases to provide diet for.")
            return []

        # Fetch the precautions for the predicted disease (async)
        predicted_label = await get_diet(diseases_name)

        if predicted_label:
            # Prepare the message with precautions
            prediction = ''
            for c, diet in enumerate(predicted_label, 1):
                if diet:  # Only include non-None precautions
                    prediction += f'Diet {c}: {diet}\n'
            
            dispatcher.utter_message(text=f"I'll provide you with some diet:\n\n{diet}")
        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find any diet for the disease.")

        return []



@sync_to_async      
def get_description(diseases_name):
    descp_obj = Description.objects.filter(Disease=diseases_name).first()
    if descp_obj:
        return (list(descp_obj.Disease_description))
    return None

class StateDescription(Action):
    def name(self) -> Text:
        return "state_description"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: dict) -> list:
        # Get the predicted disease from the slot
        diseases_name = tracker.get_slot('diseases')

        if not diseases_name:
            dispatcher.utter_message(text="I couldn't find any diseases to provide description for.")
            return []

        # Fetch the precautions for the predicted disease (async)
        predicted_label = await get_diet(diseases_name)

        if predicted_label:
            # Prepare the message with precautions
            prediction = ''
            for c, description in enumerate(predicted_label, 1):
                if description:  # Only include non-None precautions
                    prediction += f'Description {c}: {description}\n'
            
            dispatcher.utter_message(text=f"I'll provide you with some description:\n\n{description}")
        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find any description for the disease.")

        return []
