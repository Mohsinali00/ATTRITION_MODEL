# views.py

from django.shortcuts import render # type: ignore
from django.http import HttpResponse # type: ignore
import joblib
import numpy as np
import pandas as pd # Import pandas for CSV handling and data manipulation
import io # For handling in-memory file operations

from django.contrib import admin # type: ignore

from mlmodelplatform import settings
from .models.signup import User_Detail

from django.core.files.storage import FileSystemStorage # type: ignore
import os
# from PIL import Image      
# import imagehash      # type: ignore


# # --- Default Model Parameters (PLACEHOLDERS - REPLACE WITH ACTUAL TRAINED VALUES) ---
# # These values are illustrative. You MUST replace them with the values obtained
# # from training your model in Sales_predction.ipynb.
# # If your model.pkl contains these, the code will use those.
# # Otherwise, these defaults will be used.

def home(request):
    print("hello hii i am karadiya haiderali")
    return render(request, "index.html")


def DATA(request):
    return render(request, "DATA.html")

def signup(request):
    return render(request, "signup.html")

# def compare_licenses_perceptual(uploaded_path, default_path, hash_size=8, threshold=10):
#     """
#     Compares two images using perceptual hashing.

#     Args:
#         uploaded_path (str): Path to the user-uploaded license image.
#         default_path (str): Path to the backend's default license image.
#         hash_size (int): The size of the hash. Larger means more detail, less tolerance for changes.
#                          Commonly 8 or 16.
#         threshold (int): The maximum Hamming distance allowed for images to be considered a match.
#                          Lower means stricter match. Typical values for aHash/dHash are 0-10.

#     Returns:
#         bool: True if images are considered a match, False otherwise.
#     """
#     try:
#         # Open images
#         with Image.open(uploaded_path) as uploaded_img, Image.open(default_path) as default_img:
#             # Calculate perceptual hashes (using average_hash is a good general choice)
#             uploaded_hash = imagehash.average_hash(uploaded_img, hash_size=hash_size)
#             default_hash = imagehash.average_hash(default_img, hash_size=hash_size)

#             # Calculate the Hamming distance between the hashes
#             hash_distance = uploaded_hash - default_hash # This calculates Hamming distance

#             print(f"Uploaded Hash: {uploaded_hash}")
#             print(f"Default Hash:  {default_hash}")
#             print(f"Hash Distance: {hash_distance}")
#             print(f"Threshold:     {threshold}")

#             # Compare the distance to the threshold
#             if hash_distance <= threshold:
#                 return True
#             else:
#                 return False

#     except FileNotFoundError:
#         print("Error: One of the license files not found for hashing.")
#         return False
#     except Exception as e:
#         print(f"An error occurred during perceptual hash comparison: {e}")
#         return False

# --- Your existing userdata_view with license logic integrated ---
    def userdata_view(request):
        # Initialize authorization status. This will be passed to the template.
        # It's good to have a default state for GET requests or initial page load.
        is_license_authorized = False 
        
        if request.method == 'POST':
            # 1. Retrieve data from the form
            company_name = request.POST.get('companyName')
            company_phone = request.POST.get('companyNo')
            email = request.POST.get('email')
            department = request.POST.get('department')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirmPassword')
            profile_photo = request.FILES.get('profilePhoto') # For profile photo file upload
            license_image_file = request.FILES.get('licenseFile') # For license image file upload

            # Store in session (as per your context processor needs)
            request.session['profile_name'] = username
            request.session['companyname'] = company_name

            # 2. Basic Validation (add more robust validation as needed)
            if password != confirm_password:
                # messages.error(request, "Passwords do not match!") # type: ignore
                # Pass authorization status even if there's a validation error
                return render(request, 'signup.html', {'is_license_authorized': is_license_authorized})
            
            if User_Detail.objects.filter(gmail=email).exists():
                # messages.error(request, "Email already registered!") # type: ignore
                return render(request, 'signup.html', {'is_license_authorized': is_license_authorized})
            
            if User_Detail.objects.filter(user_name=username).exists():
                # messages.error(request, "Username already taken!") # type: ignore
                return render(request, 'signup.html', {'is_license_authorized': is_license_authorized})
            
            try:
                # --- License Authorization Logic ---
                if license_image_file:
                    fs_licenses = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp_uploaded_licenses'))
                    
                    # Ensure the directory for temporary uploads exists
                    if not os.path.exists(fs_licenses.location):
                        os.makedirs(fs_licenses.location)

                    uploaded_filename = fs_licenses.save(license_image_file.name, license_image_file)
                    uploaded_file_path = os.path.join(fs_licenses.location, uploaded_filename)

                    default_license_path = os.path.join(settings.MEDIA_ROOT, 'default_licenses', 'default_license.jpg') 
                    # ^^^^^ Make sure 'default_license.jpg' is the exact name of your reference file

                    # if os.path.exists(default_license_path):
                    #     is_license_authorized = compare_licenses_perceptual(uploaded_file_path, default_license_path)
                    #     request.session['license_authorized'] = is_license_authorized
                    #     if is_license_authorized:
                    #         print("User's license image matched the default.")
                    #         # messages.success(request, "License verified!")
                    #     else:
                    #         print("User's license image did NOT match the default.")
                    #         # messages.warning(request, "License could not be verified.")
                    # else:
                    #     is_license_authorized = False
                    #     request.session['license_authorized'] = False
                    #     print(f"Error: Default license image not found at {default_license_path}")
                    #     # messages.error(request, "Server error: Default license for comparison not found.")
                    
                    # Clean up the temporarily uploaded license file after comparison
                    if os.path.exists(uploaded_file_path):
                        fs_licenses.delete(uploaded_filename)
                        print(f"Deleted temporary uploaded license: {uploaded_filename}")
                else:
                    is_license_authorized = False
                    request.session['license_authorized'] = False
                    print("No license file was uploaded by the user.")
                    # messages.info(request, "No license file was provided.")


                # --- Continue with User_Detail object creation and saving ---
                hashed_password = password # In a real app, use Django's make_password: `from django.contrib.auth.hashers import make_password; hashed_password = make_password(password)`
                
                user = User_Detail(
                    companyname=company_name,
                    companyphone=company_phone,
                    gmail=email,
                    department=department,
                    user_name=username,
                    password=hashed_password, 
                    image=profile_photo, # Save the uploaded profile image
                    # Assuming your User_Detail model has a field to store authorization status
                    # You might add a field like 'is_license_verified = models.BooleanField(default=False)'
                    # is_license_verified = is_license_authorized 
                )
                user.save()

                # messages.success(request, "Account created successfully!") # type: ignore 
                # If you want to show success message and then redirect
                return render(request,'HOME.html') # Make sure 'HOME' is a valid URL name in your urls.py

            except Exception as e:
                # messages.error(request, f"An error occurred: {e}") # type: ignore
                # Pass authorization status even if there's an error
                return render(request, 'signup.html', {'is_license_authorized': is_license_authorized})
        
        # If it's a GET request, just render the empty form
        # Pass initial authorization status (false by default)
        return render(request, 'signup.html', {'is_license_authorized': is_license_authorized})


def about_logout(request):
    return render(request, "about_logout.html")

def login(request):
    return render(request, "login.html")

def logout(request):
     
     if 'profile_name' in request.session:
        print(f"Session before deletion: {request.session.items()}")
        del request.session['profile_name']
        del request.session['companyname']
        print("profile_name deleted from session.")
        print(f"Session after deletion: {request.session.items()}")
        request.session.save()  # Explicitly save the session
        return render(request,"HOME.html",{'model_loaded': True})
    


########################

import os
import joblib
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'working', 'model_files')

# Load model files once
cat_model = joblib.load(os.path.join(MODEL_DIR, 'cat_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
label_encoders = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))

def predict_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        action = request.POST.get('action')  # Check which button was clicked
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        file_path = fs.save(csv_file.name, csv_file)
        full_path = fs.path(file_path)

        try:
            df = pd.read_csv(full_path)
        except Exception as e:
            return render(request, 'HOME.html', {'error_message': 'Invalid CSV file format.'})

        if action == 'view_original':
            html_table = df.to_html(classes="table table-bordered", index=False)
            return render(request, 'HOME.html', {
                'original_table_html': html_table,
                'original_file_name': csv_file.name,
                'model_loaded': True
            })

        elif action == 'predict':
            for col, le in label_encoders.items():
                if col in df.columns:
                    try:
                        df[col] = le.transform(df[col].astype(str))
                    except Exception:
                        return render(request, 'HOME.html', {'error_message': f'Encoding failed for column: {col}'})

            try:
                df_scaled = scaler.transform(df)
            except Exception:
                return render(request, 'HOME.html', {'error_message': 'Scaling failed. Check your columns.'})

            probabilities = cat_model.predict_proba(df_scaled)[:, 1]
            predictions = (probabilities >= 0.3).astype(int)

            df['Attrition_Probability'] = probabilities
            df['Attrition_Predicted'] = predictions
            predicted_html = df[['Attrition_Predicted', 'Attrition_Probability']].to_html(classes="table table-bordered", index=False)

            return render(request, 'HOME.html', {
                'predicted_table_html': predicted_html,
                'original_file_name': csv_file.name,
                'model_loaded': True
            })

    return render(request, 'HOME.html', {'model_loaded': True})

