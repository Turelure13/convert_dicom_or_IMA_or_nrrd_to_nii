# import os
# import pydicom
import nibabel as nib
import nrrd
import numpy as np
# import dicom2nifti
#
# if __name__ == '__main__':
#
#     # Specify the input DICOM directory and output NIfTI file
#     dicom_directory = './MRIs/PHD7/PHD7_ZFI_SERIES16'
#     nifti_file = './MRIs/PHD7/nii'
#
#     try:
#         os.mkdir(nifti_file)
#     except FileExistsError:
#         print(f"The directory {nifti_file} already exists.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#     # Convert DICOM to NIfTI
#     dicom2nifti.convert_directory(dicom_directory, nifti_file, compression=False, reorient=True)

import os
import dicom2nifti


def convert_to_nifti(dicom_directory, nifti_directory):
    try:
        os.makedirs(nifti_directory, exist_ok=True)
    except Exception as e:
        print(f"An error occurred while creating the output directory: {e}")
        return

    for root, dirs, files in os.walk(dicom_directory):
        if any(file.endswith(('.dcm')) for file in files):
            output_file = os.path.join(nifti_directory, os.path.relpath(root, dicom_directory))
            try:
                try:
                    os.makedirs(output_file, exist_ok=True)
                except Exception as e:
                    print(f"An error occurred while creating the output directory: {e}")
                    return
                dicom2nifti.convert_directory(root, output_file, compression=False, reorient=True)
                print(f"Converted files in {root} to {output_file}")
            except Exception as e:
                print(f"An error occurred while converting files in {root}: {e}")
        if any(file.endswith(('.IMA')) for file in files):
            output_file = os.path.join(nifti_directory, os.path.relpath(root, dicom_directory))
            try:
                try:
                    os.makedirs(output_file, exist_ok=True)
                except Exception as e:
                    print(f"An error occurred while creating the output directory: {e}")
                    return
                dicom2nifti.convert_directory(root, output_file, compression=False, reorient=True)
                print(f"Converted files in {root} to {output_file}")
            except Exception as e:
                print(f"An error occurred while converting files in {root}: {e}")
        if any(file.endswith(('.nrrd')) for file in files):
            for file in files:
                if file.endswith('nrrd') == True:
                    output_file = os.path.join(nifti_directory, os.path.relpath(root, dicom_directory),
                                               os.path.splitext(file)[0] + '.nii')
                    try:
                        try:
                            os.makedirs(os.path.join(nifti_directory, os.path.relpath(root, dicom_directory)),
                                        exist_ok=True)
                        except Exception as e:
                            print(f"An error occurred while creating the output directory: {e}")
                            return
                        # Load the NRRD file
                        nrrd_image, nrrd_header = nrrd.read(os.path.join(root, file))
                        nii_image = nib.Nifti1Image(nrrd_image, np.eye(4))
                        # Save it as a NIfTI file
                        nib.save(nii_image, output_file)
                        os.remove(os.path.join(root, file))
                        print(f"Converted files in {root} to {output_file}")
                    except Exception as e:
                        print(f"An error occurred while converting files in {root}: {e}")

        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith('.zip'):
                try:
                    os.remove(file_path)
                    print(f"Deleted {file}")
                except Exception as e:
                    print(f"An error occurred while deleting {file}: {e}")


if __name__ == '__main__':
    main_directory = '/Users/arthurlefebvre/Downloads/UU_P4_Pre'
    nifti_output_directory = '/Users/arthurlefebvre/Downloads/UU_P4_Pre_bis'

    convert_to_nifti(main_directory, nifti_output_directory)
