import speech_recognition as sr
import csv
from persiantools import digits


r = sr.Recognizer()


class HopGame:
    def __init__(self, num_players=4, hop_value=5, save_results=False):
        self.num_players = num_players
        self.hop_value = hop_value
        self.players = []
        self.save_results = save_results
        
                
    def get_players(self):

        print(f"Game is going to start with {self.num_players}, Hop is {self.hop_value}\nGood Luck!")
        
        for i in range(self.num_players):
            print("-------------- Next Player --------------")
            print(f"PLAYER{i+1}, Say your name loud and clear!")
            player = self.talk()
            self.players.append({"name": player, "alive": True, "numbers": []}) 
            
               
    def start_game(self):
        
        print("---------------------------- GAME STARTED ----------------------------")
        print(f"Players: {[p["name"] for p in self.players]}")

        number = 1
        player_index = 0
        
        while True:
            
            player_index = player_index % self.num_players
            
            if winner :=self.check_winner():
                print(f"Winner is {winner["name"]} 👑")
                break
            
            current_player = self.players[player_index]

            if current_player["alive"] == False:
                player_index += 1
                continue
            
            print("----------")
            print(f"{current_player["name"]}: ")
            word = self.talk()
            en_num = digits.fa_to_en(word)
            print(word, "-->", en_num)
            
            if number % self.hop_value == 0 and "هوپ" not in word: 
                print(f"{current_player["name"]} is eliminated ❌")
                current_player["alive"] = False
                
            if number % self.hop_value != 0 and str(number) not in en_num:
                print(f"{current_player["name"]} is eliminated ❌")
                current_player["alive"] = False
            
            current_player["numbers"].append(en_num)
            number += 1
            player_index += 1

    
    def talk(self):
        while True:
            with sr.Microphone(sample_rate=44000) as source:
                print("Listening 🎙️")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
                try:
                    # Get New Api key , each free key is limited to 50 uses per day! https://www.chromium.org/developers/how-tos/api-keys/    
                    result = r.recognize_google(audio, language="fa-IR")
                    return result
                    
                except sr.UnknownValueError:
                    print("I cant hear you 👂 say it again❔")
                except sr.RequestError:
                    print("Request Failed: Check your internet connection or API.")
            

    def check_winner(self):
        winner = 0
        for p in self.players:
            if p["alive"] == True:
                winner += 1
        
        if winner == 1:
            for winner in self.players:
                if winner["alive"] == True:
                    if self.save_results == True: self.save()
                    return winner  
         
            
    def save(self):
        with open("result.csv", "w") as f:
            writer = csv.writer(f, list(self.players[0].keys()))
            for p in self.players:
                writer.writerow([p["name"], p["alive"], p["numbers"]]) 
            
        
            
if __name__ == "__main__":
    num_players = int(input("Number of players: "))
    hop_value = int(input("Hop value: "))
    sv = input("Do you want to save results [Y/N]? ")
    sv = True if sv.lower() == 'y' else False
    
    game1 = HopGame(num_players=num_players, hop_value=hop_value, save_results=sv)
    game1.get_players()
    game1.start_game()
    