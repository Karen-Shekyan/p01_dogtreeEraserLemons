let autocomplete = (inp, arr) => {
    let currentFocus;
    inp.addEventListener("input", function(e) {
      let a, b, i, val = this.value;
      closeAllLists();
      if (!val) {
        return false;
      }
      currentFocus = -1;
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items list-group text-left");
      this.parentNode.appendChild(a);
      for (i = 0; i < arr.length; i++) {
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          b = document.createElement("DIV");
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          b.addEventListener("click", function(e) {
            inp.value = this.getElementsByTagName("input")[0].value;
            closeAllLists();
          });
          a.appendChild(b);
        }
      }
    });

    inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) {
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) {
        e.preventDefault();
        if (currentFocus > -1) {
          if (x) x[currentFocus].click();
        }
      }
    });

    // methods used for autocomplete
    let addActive = (x) => {
      if (!x) return false;
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = x.length - 1;
      x[currentFocus].classList.add("active");
    }
    let removeActive = (x) => {
      for (let i = 0; i < x.length; i++) {
        x[i].classList.remove("active");
      }
    }
    let closeAllLists = (elmt) => {
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmt != x[i] && elmt != inp) {
          x[i].parentNode.removeChild(x[i]);
      }
    }
  }

  document.addEventListener("click", function(e) {
    closeAllLists(e.target);
  });
};

// database connection
/* const sqlite3 = require("sqlite3").verbose();
let db = new sqlite3.Database('/app/character.db', sqlite3.OPEN_READ);
let sql = 'SELECT * FROM heroes';
let heroes = [];
db.all(sql, [], (err, rows) => {
  if (err) { throw err };
  rows.forEach((row) => {
    heroes.push(row.name);
  });
});
db.close(); */

// this is an example; if you type hello into the search bar itll show up
let heroes = ['A-Bomb', 'Abe Sapien', 'Abin Sur', 'Abomination', 'Abraxas', 'Absorbing Man', 'Adam Monroe', 'Adam Strange', 'Agent Bob', 'Agent Zero', 'Air-Walker', 'Ajax', 'Alan Scott', 'Alex Mercer', 'Alfred Pennyworth', 'Alien', 'Amazo', 'Angel', 'Angel Dust', 'Angel Salvadore', 'Animal Man', 'Annihilus', 'Ant-Man', 'Ant-Man II', 'Anti-Monitor', 'Anti-Venom', 'Apocalypse', 'Aquababy', 'Aqualad', 'Aquaman', 'Arachne', 'Archangel', 'Arclight', 'Ardina', 'Ares', 'Ariel', 'Armor', 'Atlas', 'Atom Girl', 'Atom II', 'Aurora', 'Azazel', 'Azrael', 'Bane', 'Banshee', 'Bantam', 'Batgirl', 'Batgirl IV', 'Batgirl VI', 'Batman', 'Batman II', 'Battlestar', 'Batwoman V', 'Beast Boy', 'Beta Ray Bill', 'Beyonder', 'Big Barda', 'Big Daddy', 'Big Man', 'Bill Harken', 'Bionic Woman', 'Bird-Brain', 'Bishop', 'Bizarro', 'Black Adam', 'Black Bolt', 'Black Canary', 'Black Cat', 'Black Flash', 'Black Knight III', 'Black Lightning', 'Black Mamba', 'Black Manta', 'Black Panther', 'Black Widow', 'Blackout', 'Blackwing', 'Blackwulf', 'Blade', 'Bling!', 'Blink', 'Blizzard II', 'Blob', 'Bloodaxe', 'Bloodhawk', 'Blue Beetle III', 'Boba Fett', 'Boom-Boom', 'Brainiac', 'Brainiac 5', 'Brundlefly', 'Buffy', 'Bullseye', 'Bumblebee', 'Bushido', 'Cable', 'Callisto', 'Cameron Hicks', 'Cannonball', 'Captain America', 'Captain Atom', 'Captain Britain', 'Captain Cold', 'Captain Hindsight', 'Captain Marvel', 'Captain Marvel II', 'Captain Planet', 'Carnage', 'Catwoman', 'Century', 'Chamber', 'Chameleon', 'Changeling', 'Cheetah', 'Cheetah III', 'Chuck Norris', 'Citizen Steel', 'Claire Bennet', 'Cloak', 'Clock King', 'Colossus', 'Copycat', 'Cottonmouth', 'Crystal', 'Cyborg', 'Cyborg Superman', 'Cyclops', 'DL Hawkins', 'Dagger', 'Daphne Powell', 'Daredevil', 'Darkhawk', 'Darkman', 'Darkseid', 'Darkstar', 'Darth Maul', 'Darth Vader', 'Dash', 'Data', 'Dazzler', 'Deadman', 'Deadpool', 'Deadshot', 'Deathlok', 'Deathstroke', 'Demogoblin', 'Destroyer', 'Diamondback', 'Doc Samson', 'Doctor Doom', 'Doctor Fate', 'Doctor Octopus', 'Doctor Strange', 'Domino', 'Donatello', 'Doomsday', 'Doppelganger', 'Dormammu', 'Dr Manhattan', 'Drax the Destroyer', 'Ego', 'Elastigirl', 'Electro', 'Elektra', 'Elle Bishop', 'Elongated Man', 'Emma Frost', 'Enchantress', 'Ethan Hunt', 'Etrigan', 'Evil Deadpool', 'Evilhawk', 'Exodus', 'Falcon', 'Fallen One II', 'Faora', 'Feral', 'Fin Fang Foom', 'Firebird', 'Firelord', 'Firestar', 'Firestorm', 'Flash', 'Flash II', 'Flash III', 'Flash IV', 'Forge', 'Franklin Richards', 'Franklin Storm', 'Frenzy', 'Galactus', 'Gambit', 'Gamora', 'Gary Bell', 'General Zod', 'Ghost Rider', 'Giganta', 'Gladiator', 'Goblin Queen', 'Godzilla', 'Gog', 'Goku', 'Gorilla Grodd', 'Gravity', 'Greedo', 'Green Arrow', 'Green Goblin', 'Green Goblin II', 'Groot', 'Guy Gardner', 'Hal Jordan', 'Han Solo', 'Hancock', 'Harley Quinn', 'Harry Potter', 'Havok', 'Hawk', 'Hawkeye', 'Hawkeye II', 'Hawkgirl', 'Heat Wave', 'Hela', 'Hellboy', 'Hellcat', 'Hercules', 'Hit-Girl', 'Hope Summers', 'Hulk', 'Human Torch', 'Huntress', 'Husk', 'Hybrid', 'Hydro-Man', 'Hyperion', 'Iceman', 'Impulse', 'Indiana Jones', 'Indigo', 'Ink', 'Invisible Woman', 'Iron Fist', 'Iron Man', 'Iron Monger', 'Isis', 'JJ Powell', 'Jack of Hearts', 'Jack-Jack', 'James Bond', 'James T. Kirk', 'Jar Jar Binks', 'Jason Bourne', 'Jean Grey', 'Jean-Luc Picard', 'Jennifer Kale', 'Jessica Cruz', 'Jessica Jones', 'Jim Powell', 'John Constantine', 'John Wraith', 'Joker', 'Jolt', 'Jubilee', 'Judge Dredd', 'Juggernaut', 'Junkpile', 'Justice', 'Kang', 'Kathryn Janeway', 'Katniss Everdeen', 'Kevin 11', 'Kick-Ass', 'Kid Flash', 'Killer Croc', 'Killer Frost', 'Kilowog', 'King Kong', 'King Shark', 'Kingpin', 'Klaw', 'Kool-Aid Man', 'Kraven II', 'Kraven the Hunter', 'Krypto', 'Kyle Rayner', 'Kylo Ren', 'Lady Deathstrike', 'Leader', 'Leech', 'Legion', 'Leonardo', 'Lex Luthor', 'Light Lass', 'Lightning Lad', 'Lightning Lord', 'Living Brain', 'Living Tribunal', 'Lizard', 'Lobo', 'Loki', 'Longshot', 'Luke Cage', 'Luke Skywalker', 'Luna', 'MODOK', 'Mach-IV', 'Machine Man', 'Magneto', 'Magog', 'Magus', 'Man of Miracles', 'Man-Bat', 'Man-Thing', 'Man-Wolf', 'Mandarin', 'Mantis', 'Martian Manhunter', 'Marvel Girl', 'Master Chief', 'Match', 'Matt Parkman', 'Maverick', 'Maxima', 'Maya Herrera', 'Medusa', 'Meltdown', 'Mephisto', 'Mera', 'Metallo', 'Metron', 'Micah Sanders', 'Michelangelo', 'Micro Lad', 'Mimic', 'Misfit', 'Miss Martian', 'Mister Fantastic', 'Mister Freeze', 'Mister Knife', 'Mister Mxyzptlk', 'Mister Sinister', 'Mister Zsasz', 'Mockingbird', 'Molten Man', 'Monica Dawson', 'Moon Knight', 'Moonstone', 'Morlun', 'Moses Magnum', 'Mr Immortal', 'Mr Incredible', 'Ms Marvel II', 'Multiple Man', 'Mysterio', 'Mystique', 'Namor', 'Namora', 'Namorita', 'Naruto Uzumaki', 'Nebula', 'Negasonic Teenage Warhead', 'Nick Fury', 'Nightcrawler', 'Nightwing', 'Niki Sanders', 'Nina Theroux', 'Northstar', 'Nova', 'Odin', 'Offspring', 'One Punch Man', 'One-Above-All', 'Onslaught', 'Oracle', 'Osiris', 'Ozymandias', 'Parademon', 'Paul Blart', 'Penguin', 'Phantom Girl', 'Phoenix', 'Plantman', 'Plastic Man', 'Plastique', 'Poison Ivy', 'Polaris', 'Power Girl', 'Predator', 'Professor X', 'Professor Zoom', 'Psylocke', 'Punisher', 'Purple Man', 'Pyro', 'Q', 'Question', 'Quicksilver', 'Quill', "Ra's Al Ghul", 'Rachel Pirzad', 'Rambo', 'Raphael', 'Raven', 'Ray', 'Red Arrow', 'Red Hood', 'Red Hulk', 'Red Mist', 'Red Robin', 'Red Skull', 'Red Tornado', 'Rey', 'Rhino', 'Rick Flag', 'Riddler', 'Rip Hunter', 'Robin', 'Robin II', 'Robin III', 'Robin V', 'Robin VI', 'Rocket Raccoon', 'Rogue', 'Ronin', 'Rorschach', 'Sabretooth', 'Sage', 'Sandman', 'Sasquatch', 'Sauron', 'Savage Dragon', 'Scarecrow', 'Scarlet Spider', 'Scarlet Spider II', 'Scarlet Witch', 'Scorpia', 'Scorpion', 'Sebastian Shaw', 'Sentry', 'Shadow King', 'Shadow Lass', 'Shadowcat', 'Shang-Chi', 'Shatterstar', 'She-Hulk', 'She-Thing', 'Shocker', 'Shriek', 'Sif', 'Silk', 'Silver Surfer', 'Silverclaw', 'Simon Baz', 'Sinestro', 'Siren', 'Siryn', 'Skaar', 'Snowbird', 'Sobek', 'Solomon Grundy', 'Songbird', 'Space Ghost', 'Spawn', 'Spectre', 'Speedy', 'Spider-Girl', 'Spider-Gwen', 'Spider-Man', 'Spider-Woman', 'Spider-Woman III', 'Spock', 'Spyke', 'Star-Lord', 'Stardust', 'Starfire', 'Stargirl', 'Static', 'Steel', 'Stephanie Powell', 'Steppenwolf', 'Storm', 'Stormtrooper', 'Sunspot', 'Superboy', 'Superboy-Prime', 'Supergirl', 'Superman', 'Swamp Thing', 'Swarm', 'Sylar', 'Synch', 'T-1000', 'T-800', 'T-850', 'T-X', 'Taskmaster', 'Tempest', 'Thanos', 'The Cape', 'The Comedian', 'Thing', 'Thor', 'Thor Girl', 'Thunderbird', 'Thunderstrike', 'Thundra', 'Tiger Shark', 'Tigra', 'Tinkerer', 'Toad', 'Toxin', 'Triplicate Girl', 'Triton', 'Two-Face', 'Ultragirl', 'Ultron', 'Utgard-Loki', 'Vanisher', 'Vegeta', 'Venom', 'Venom II', 'Venom III', 'Venompool', 'Vibe', 'Vindicator', 'Violet Parr', 'Vision', 'Vixen', 'Vulture', 'Walrus', 'War Machine', 'Warlock', 'Warp', 'Warpath', 'Wasp', 'Watcher', 'White Canary', 'Wildfire', 'Winter Soldier', 'Wolfsbane', 'Wolverine', 'Wonder Girl', 'Wonder Man', 'Wonder Woman', 'Wyatt Wingfoot', 'X-23', 'X-Man', 'Yellowjacket', 'Yellowjacket II', 'Ymir', 'Yoda', 'Zatanna', 'Zoom']

autocomplete(document.getElementById("myInput"), heroes);