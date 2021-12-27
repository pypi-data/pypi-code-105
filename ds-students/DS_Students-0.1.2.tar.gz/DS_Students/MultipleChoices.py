def MultipleChoice(description, options, correct_answer):
    """Creates multiple choice functionality"""
    
    import ipywidgets as widgets
    import sys
    from IPython.display import display
    from IPython.display import clear_output
    
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternative = widgets.RadioButtons(
        layout={'width': 'max-content'},
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternative.value)
        if a==correct_answer_index:
            s = '\x1b[6;30;42m' + "Correct!" + '\x1b[0m' +"\n" #green color
        else:
            s = '\x1b[5;30;41m' + "Incorrect" + '\x1b[0m' +"\n" #red color
        with feedback_out:
            clear_output()
            print(s)
        return
    
    check = widgets.Button(description="submit")
    check.on_click(check_selection)
    
    
    return widgets.VBox([description_out, alternative, check, feedback_out])



def MC(description, options, correct_answer,cor, incor):
    """Creates multiple choice functionality"""
    
    
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    import sys
    
    
    if correct_answer not in options:
        options.append(correct_answer)
    
    correct_answer_index = options.index(correct_answer)
    
    radio_options = [(words, i) for i, words in enumerate(options)]
    alternative = widgets.RadioButtons(
        layout={'width': 'max-content'},
        options = radio_options,
        description = '',
        disabled = False
    )
    
    description_out = widgets.Output()
    with description_out:
        print(description)
        
    feedback_out = widgets.Output()

    def check_selection(b):
        a = int(alternative.value)
        if a==correct_answer_index:
            s = '\x1b[1;30;42m' + "Correct!" + '\x1b[0m' +"\n" #green color
            with feedback_out:
                clear_output()
                print(s,cor)
                return
        else:
            s = '\x1b[1;30;41m' + "Incorrect" + '\x1b[0m' +"\n" #red color
        with feedback_out:
            clear_output()
            print(s,incor)
        return
    
    check = widgets.Button(description="submit")
    check.on_click(check_selection)
    
    
    return widgets.VBox([description_out, alternative, check, feedback_out])


# #This is for testing..

# from IPython.display import display
# Q1 = MultipleChoice(' Which of these fruits start with the letter A?',['Apples','Bananas','Strawberries'],'Apples')
# Q2 = MultipleChoice('Which of these animals bark?',['cat','dog','mouse'],'dog')
# Q3 = MultipleChoice('What is the color of the sky?',['blue','white','red'],'blue')
# display(Q1, Q2,Q3)


# Q1 = MC(' Which of these fruits start with the letter A?',['Apples','Bananas','Strawberries'],'Apples',cor="Fun Fact: Over 2,500 varieties of apples are grown in the United States!!", incor= "Sorry.. try again!")
# Q2 = MC('Which of these animals bark?',['cat','dog','mouse'],'dog',cor="This is why your answer is correct!!", incor= "This is why your answer is wrong")
# Q3 = MC('What is the color of the sky?',['blue','white','red'],'white',cor="This is why your answer is correct!!", incor= "This is why your answer is wrong")
# display(Q1, Q2,Q3)