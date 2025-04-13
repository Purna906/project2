import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

class VotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Voting System")
        self.root.geometry("800x600")

        self.max_votes = 8
        self.total_votes = 0
        self.votes = [0, 0]  # Secretly tracked
        self.candidate_names = ["", ""]
        self.candidate_images = [None, None]
        self.image_paths = ["", ""]

        self.setup_table()

    def setup_table(self):
        tk.Label(self.root, text="Enter Candidate Details", font=("Arial", 16, "bold")).pack(pady=10)

        self.table_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        self.table_frame.pack(pady=10)

        self.entries = []

        for i in range(2):
            frame = tk.Frame(self.table_frame, bd=1, relief=tk.SOLID, padx=10, pady=10)
            frame.grid(row=0, column=i, padx=30, pady=20)

            tk.Label(frame, text=f"Candidate {i+1}", font=("Arial", 12)).pack()
            name_entry = tk.Entry(frame, width=25)
            name_entry.pack(pady=5)
            img_btn = tk.Button(frame, text="Upload Image", command=lambda idx=i: self.upload_image(idx))
            img_btn.pack(pady=5)
            setattr(self, f"name_entry_{i}", name_entry)
            self.entries.append((name_entry, img_btn))

        tk.Button(self.root, text="Submit Candidates", font=("Arial", 12), command=self.submit_candidates).pack(pady=15)

    def upload_image(self, index):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            image = Image.open(file_path).resize((100, 100))
            self.candidate_images[index] = ImageTk.PhotoImage(image)
            self.image_paths[index] = file_path
            label = tk.Label(self.entries[index][1].master, image=self.candidate_images[index])
            label.image = self.candidate_images[index]
            label.pack()

    def submit_candidates(self):
        name1 = self.name_entry_0.get().strip()
        name2 = self.name_entry_1.get().strip()

        if not name1 or not name2 or not self.image_paths[0] or not self.image_paths[1]:
            messagebox.showerror("Input Error", "Please fill names and upload images for both candidates.")
            return

        self.candidate_names = [name1, name2]
        self.table_frame.destroy()
        self.start_voting()

    def start_voting(self):
        tk.Label(self.root, text="Vote for Your Favorite Candidate", font=("Arial", 16, "bold")).pack(pady=10)

        self.vote_frame = tk.Frame(self.root)
        self.vote_frame.pack()

        for i in range(2):
            frame = tk.Frame(self.vote_frame, bd=2, relief=tk.RIDGE)
            frame.grid(row=0, column=i, padx=20)

            tk.Label(frame, text=self.candidate_names[i], font=("Arial", 14)).pack(pady=5)
            img = Image.open(self.image_paths[i]).resize((100, 100))
            photo = ImageTk.PhotoImage(img)
            self.candidate_images[i] = photo
            tk.Label(frame, image=photo).pack()
            tk.Button(frame, text="Vote", font=("Arial", 12), command=lambda idx=i: self.vote(idx)).pack(pady=10)

    def vote(self, index):
        if self.total_votes >= self.max_votes:
            messagebox.showinfo("Voting Closed", "All votes have been cast.")
            return

        self.votes[index] += 1
        self.total_votes += 1

        if self.total_votes == self.max_votes:
            messagebox.showinfo("Voting Complete", "Voting is done.\nEnter the secret code to view results.")
            self.ask_secret_code()
        else:
            messagebox.showinfo("Vote Registered", "Your vote has been recorded.")

    def ask_secret_code(self):
        code = simpledialog.askstring("Secret Code", "Enter the 3-digit secret code to unlock results:")
        if code == "123":
            self.show_result()
        else:
            messagebox.showwarning("Access Denied", "Incorrect code. Voting results are locked.")

    def show_result(self):
        total = sum(self.votes)
        if total == 0:
            messagebox.showinfo("Results", "No votes were cast.")
            return

        percent1 = (self.votes[0] / total) * 100
        percent2 = (self.votes[1] / total) * 100

        if self.votes[0] > self.votes[1]:
            winner = self.candidate_names[0]
        elif self.votes[1] > self.votes[0]:
            winner = self.candidate_names[1]
        else:
            winner = "It's a Tie!"

        result_text = (
            f"{self.candidate_names[0]}: {self.votes[0]} votes ({percent1:.2f}%)\n"
            f"{self.candidate_names[1]}: {self.votes[1]} votes ({percent2:.2f}%)\n\n"
            f"🏆 Winner: {winner}"
        )

        messagebox.showinfo("Final Results", result_text)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = VotingSystem(root)
    root.mainloop()
