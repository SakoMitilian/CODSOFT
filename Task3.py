from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import torch

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Check if GPU is available for faster processing
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

class ImageCaptioningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task 3: Advanced Image Captioning")
        self.root.geometry("600x600")

        # Heading
        self.heading = tk.Label(root, text="Advanced Image Captioning", font=("Arial", 18))
        self.heading.pack(pady=20)

        # Upload button
        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        # Display area for image
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Caption display
        self.caption_label = tk.Label(root, text="", font=("Arial", 12), wraplength=500, justify="center")
        self.caption_label.pack(pady=10)

        # Save button (disabled initially)
        self.save_btn = tk.Button(root, text="Save Image with Caption", command=self.save_captioned_image, state=tk.DISABLED)
        self.save_btn.pack(pady=10)

    def upload_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        # Load and display the selected image
        try:
            self.image = Image.open(file_path)
            img = self.image.resize((300, 300))
            self.img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.img_tk)
            self.caption_label.config(text="Generating caption...")
            self.root.update()

            # Generate and display caption
            caption = self.generate_caption(self.image)
            self.caption_label.config(text=f"Caption: {caption}")
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def generate_caption(self, image):
        # Preprocess image and generate caption
        inputs = processor(images=image, return_tensors="pt").to(device)
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption

    def save_captioned_image(self):
        # Save the image with the caption overlayed
        try:
            img_with_caption = self.image.copy()
            caption_text = self.caption_label.cget("text").replace("Caption: ", "")
            img_draw = ImageDraw.Draw(img_with_caption)
            img_draw.text((10, img_with_caption.height - 30), caption_text, fill="white")

            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
            if save_path:
                img_with_caption.save(save_path)
                messagebox.showinfo("Saved", "Image with caption saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

# Initialize the GUI
root = tk.Tk()
app = ImageCaptioningApp(root)
root.mainloop()
