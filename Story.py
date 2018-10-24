
story = {"_default_question": "Was möchtest du tun?",
         "_prompt":"Deine Wahl: ",
         }

story["start"] = {"message":"Herzlich Wilkommen zu Grimms Kiste",
                  "question":"Welche Geschichte möchtst du Erleben",
                  "actions":[
                      {
                        "label":"Harry Potter",
                        "next":"HP1"
                      },
                      {"label":"Herr der Ringe",
                       "next":"HdR1"
                       }
                  ]
                  }
story["HP1"] = {
    "message": "Harry Potter ist in kleiner Zauberer",
    "actions": [
        {
            "label": "Ich versuche, die Tür zu öffnen",
            "next": "HP2"
        },
        {
            "label": "Ich gehe rechts um die Ecke!",
            "next": "gang2"
        }
    ]

}

story ["HP2"] ={
    "message": "Hinter der Tür ist ein Hund",
    "actions": [
        {
            "label": "Ich versuche, die Tür zu öffnen",
            "next": "ende"
        },
        {
            "label": "Ich gehe rechts um die Ecke!",
            "next": "gang2"
        }
    ]

}
story["ende"] = {
    "message": "Damit ist das Spiel zu Ende. Auf Wiedersehen."}


