import gzip
import shutil
import glob
import os
import kagglehub

if __name__ == "__main__":
    path = kagglehub.dataset_download("austro/beat-the-bookie-worldwide-football-dataset")
    gz_files = glob.glob(os.path.join(path, '*.gz'))

    # Get the data directory path (parent directory of this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = script_dir  # data/ folder is where this script is located

    if not gz_files:
        print("No .gz files found in the Kaggle download directory.")
    else:
        print(f"Found {len(gz_files)} .gz file(s) to decompress:")
        for gz_file in gz_files:
            print(f"  - {gz_file}")
        
        print(f"\nDecompressing files to {data_dir}...")
        for gz_file in gz_files:
            # Get the base filename without .gz extension
            base_filename = os.path.basename(gz_file)[:-3]  # Remove .gz extension
            output_file = os.path.join(data_dir, base_filename)
            
            # Skip if output file already exists
            if os.path.exists(output_file):
                print(f"  Skipping {gz_file} - {output_file} already exists")
                # Still delete the .gz file even if output exists
                try:
                    os.remove(gz_file)
                    print(f"  ✓ Deleted {gz_file}")
                except Exception as e:
                    print(f"  ✗ Error deleting {gz_file}: {e}")
                continue
            
            try:
                with gzip.open(gz_file, 'rb') as f_in:
                    with open(output_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                print(f"  ✓ Decompressed {gz_file} -> {output_file}")
                
                # Delete the .gz file after successful decompression
                os.remove(gz_file)
                print(f"  ✓ Deleted {gz_file}")
            except Exception as e:
                print(f"  ✗ Error decompressing {gz_file}: {e}")
        
        # Delete the Kaggle folder after all files are processed
        print(f"\nCleaning up Kaggle download folder...")
        try:
            shutil.rmtree(path)
            print(f"  ✓ Deleted Kaggle folder: {path}")
        except Exception as e:
            print(f"  ✗ Error deleting Kaggle folder {path}: {e}")

