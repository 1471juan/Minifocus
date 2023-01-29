# Module to visualize array's data in the terminal
# jmanuel.pgp@gmail.com

# https://en.m.wikipedia.org/wiki/ANSI_escape_code#Colors

class MiniPlot():

    #Returns the closest integrer 
    def floor(n):
        return int(n - (n % 1))

    #Points graph from array
    def plot(data,show_xAxis=False):
        object = ''
        #Add 1
        # data.append(1)
        # Sort the array
        data.sort(reverse=True)

        if(len(str(data[0]))>=3):
            data_divider=10
        else:
            data_divider=len(str(data[0]))
        data_compressed=[]
        #Divide by number
        i=0
        while(i<len(data)):
            data_compressed.append(MiniPlot.floor(data[i]/data_divider))
            i+=1
        element = 0
        while (element < len(data_compressed)):

            element_biggest = data_compressed[0]
            elements_before = data_compressed[element]-1
            #You have to sum the diference of the string length between the biggest and smaller element
            elements_after = element_biggest - data_compressed[element]

            tmp = str(len(data_compressed)-element) + ' |' + (' ' * elements_before) + '*' + (' ' * elements_after) + '|'+'\n'
            
            object += tmp
            element += 1

        #Add x axis with the values of the data
        if(show_xAxis):
            data.sort(reverse=False)
            data_compressed.sort(reverse=False)
            value = 0
            while (value < len(data_compressed)):
                if(value==0):
                    elements_remaining_toNext = data[value]
                    tmp = ('-' * len(str(data[value-1]))) + ('-' * elements_remaining_toNext) + str(data[value])
                else:
                    lenght_of_all_values_before_element=0
                    i=1
                    while(i<=value):
                        lenght_of_all_values_before_element+=len(str(data[i]))
                        i+=len(data_compressed)
                    elements_remaining_toNext = data_compressed[value]-data_compressed[value-1]-(lenght_of_all_values_before_element)
                    tmp = ('-' * elements_remaining_toNext) + str(data[value]) 
                object+=tmp
                value+=1


        object+='\n'
        print(object)

    #Bars graph from array
    def bar(data,data_value_name=[], sort=False):
        if sort:
            data = sorted(data)
        object = ''
        element = 0
        while (element < len(data)):
            #create line
            tmp = data_value_name[element]+'[' + str(data[element]) + ']: ' + ('*' * data[element]) + '\n'
            #add to the graph
            object += tmp
            element += 1
        #print
        print(object)
