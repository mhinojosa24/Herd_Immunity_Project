import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
from config import DEBUG_MODE as debug

class Simulation(object):
    '''
    Main class that will run the herd immunity simulation program.  Expects initialization
    parameters passed as command line arguments when file is run.
    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    _____Attributes______
    - logger: Logger object.  The helper object that will be responsible for
    writing all logs to the simulation.

    - population_size: Int.  The size of the population for this simulation.

    - population: [Person].  A list of person objects representing all people in
        the population.

    - next_person_id: Int.  The next available id value for all created
    person objects. Each person should have a unique _id value.

    - virus_name: String.  The name of the virus for the simulation.
    This will be passed to the Virus object upon instantiation.

    - mortality_rate: Float between 0 and 1.  This will be passed
    to the Virus object upon instantiation.

    - basic_repro_num: Float between 0 and 1.   This will be passed
    to the Virus object upon instantiation.

    - vacc_percentage: Float between 0 and 1.  Represents the total
    percentage of population vaccinated for the given simulation.

    - current_infected: Int.  The number of currently people in the
    population currently infected with the disease in the simulation.

    - total_infected: Int.  The running total of people that have been
    infected since the simulation began, including any people
    currently infected.

    - total_dead: Int.  The number of people that have died as a result
    of the infection during this simulation.  Starts at zero.

    _____Methods_____
    __init__(population_size, vacc_percentage, virus_name, mortality_rate,
     basic_repro_num, initial_infected=1):
        -- All arguments will be passed as command-line arguments when the file is run.
        -- After setting values for attributes, calls self._create_population() in order
            to create the population array that will be used for this simulation.
    _create_population(self, initial_infected):
        -- Expects initial_infected as an Int.
        -- Should be called only once, at the end of the __init__ method.
        -- Stores all newly created Person objects in a local variable, population.
        -- Creates all infected person objects first.  Each time a new one is created,
            increments infected_count variable by 1.
        -- Once all infected person objects are created, begins creating healthy
            person objects.  To decide if a person is vaccinated or not, generates
            a random number between 0 and 1.  If that number is smaller than
            self.vacc_percentage, new person object will be created with is_vaccinated
            set to True.  Otherwise, is_vaccinated will be set to False.
        -- Once len(population) is the same as self.population_size, returns population.
    '''

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        # Attributes when called and initalized
        self.population_size = population_size
        self.vacc_percentage = vacc_percentage
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.virus = Virus(self.virus_name, self.mortality_rate, self.basic_repro_num)

        self.population = []
        self.dead_people = 0
        self.total_infected = 0
        self.current_infected = 0
        self.next_person_id = 0
        self.newly_infected = []
        self.population = self._create_population(initial_infected)
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
        virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        print("population size:", self.population_size)
        # TODO: Create a Logger object and bind it to self.logger.  You should use this
        # logger object to log all events of any importance during the simulation. Don't forget
        # to call these logger methods in the corresponding parts of the simulation!

        # This attribute will be used to keep track of all the people that catch
        # the infection during a given time step. We'll store each newly infected
        # person's .ID attribute in here. At the end of each time step, we'll call
        # self._infect_newly_infected() and then reset .newly_infected back to an empty
        # list.

        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.

    def _create_population(self, initial_infected):
        # print("running _create_population")
        # TODO: Finish this method! This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).
        self.population = []
        self.current_infected = 0
        while len(self.population) != self.population_size:
            if self.current_infected != initial_infected:
                self.population.append(Person(self.next_person_id, False, self.virus))
                self.current_infected += 1
            else:
                # Now create all the rest of the people.
                # Every time a new person will be created, generate a random number between
                # 0 and 1. If this number is smaller than vacc_percentage, this person
                # should be created as a vaccinated person. If not, the person should be
                # created as an unvaccinated person.
                generator = random.uniform(0, 1)
                if generator < self.vacc_percentage:
                    self.population.append(Person(self.next_person_id, True))
                else:
                    self.population.append(Person(self.next_person_id, False))
            self.next_person_id += 1
            # TODO: After any Person object is created, whether sick or healthy,
            # you will need to increment self.next_person_id by 1. Each Person object's
            # ID has to be unique!
        return self.population


    # TODO: Complete this method! This method should return True if the simulation
    # should continue, or False if it should not. The simulation should end under
    # any of the following circumstances:
    #     - The entire population is dead.
    #     - There are no infected people left in the population.
    # In all other instances, the simulation should continue.
    def _simulation_should_continue(self):
        # print("running sim should continue")

        logger_file = open(self.file_name, 'a')
        logger_file.write("People who survived and did not survived\n")
        # alivePpl = 0

        for person in self.population:
            if person.infection is not None:
                person.did_survive_infection(self.mortality_rate)
            # print("THEY ALIVE?",person.is_alive)
            if not person.is_alive:
                self.dead_people += 1
            # else:
            #     alivePpl+=1

        # print("POP SIZE:",len(self.population))
        # print("alive ppl:", alivePpl)
        print("DEAD:",self.dead_people)
        if (len(self.population) - self.dead_people) < 1:
            print("The virus ceased to spread. With a population of ", (len(self.population)-self.dead_people), "still alive.")
            print()
            return False
        elif self.current_infected == 0:
            print("The virus ceased to spread. With a population of ", (len(self.population)-self.dead_people), "still alive.")
            return False

        return True



    # TODO: Finish this method. This method should run the simulation until
    # everyone in, or the disease no longer exists in the
    # population. To simplify the logic here, we will use the helper method
    # _simulation_should_continue() to tell us whether or not we should continue
    # the simulation and run at least 1 more time_step.
    # This method should keep track of the number of time steps that
    # have passed using the time_step_counter variable. Make sure you remember
    # the logger's log_time_step() method at the end of each time step, pass in the
    # time_step_counter variable!
    # TODO: Remember to set this variable to an intial call of
    # self._simulation_should_continue()!
    # TODO: for every iteration of this loop, call self.time_step() to compute another
    # round of this simulation. At the end of each iteration of this loop, remember
    # to rebind should_continue to another call of self._simulation_should_continue()!
    def run(self):
        # print("running run")
        time_step_counter = 0
        should_continue = True
        while should_continue:
            # print("in while loop")
            self.time_step()
            # print("time step called")
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()
            # print("should_continue now:", should_continue)
        print('The simulation has ended after {} turns.'.format(time_step_counter))

    # TODO: Finish this method!  This method should contain all the basic logic
    # for computing one time step in the simulation.  This includes:
        # - For each infected person in the population:
        #        - Repeat for 100 total interactions:
        #             - Grab a random person from the population.
        #           - If the person is dead, continue and grab another new
        #                 person from the population. Since we don't interact
        #                 with dead people, this does not count as an interaction.
        #           - Else:
        #               - Call simulation.interaction(person, random_person)
        #               - Increment interaction counter by 1.
    def time_step(self):
        infected_people = [person for person in self.population if person.is_alive and person.infection != None]
        healthy_people = [person for person in self.population if not person.infection and person.is_alive]
        time_count = 0

        for sick_person in infected_people:
            while time_count <= 100:
                random_healthy_person = random.choice(healthy_people)
                simulation.interaction(sick_person, random_healthy_person)
                time_count += 1
            sick_person.did_survive_infection
            self.logger.log_infection_survival(sick_person,sick_person.did_survive_infection(self.mortality_rate))

        self._infect_newly_infected()


    def interaction(self, sick_person, random_person):
        # TODO: Finish this method! This method should be called any time two living
        # people are selected for an interaction. That means that only living people
        # should be passed into this method.  Assert statements are included to make sure
        # that this doesn't happen.
        # The possible cases you'll need to cover are listed below:
        #1 random_person is vaccinated:
        #     nothing happens to random person.
        # random_person is already infected:
        #     nothing happens to random person.
        # random_person is healthy, but unvaccinated:
        #     generate a random number between 0 and 1.  If that number is smaller
        #     than basic_repro_num, random_person's ID should be appended to
        #     Simulation object's newly_infected array, so that their .infected
        #     attribute can be changed to True at the end of the time step.
        # TODO: Remember to call self.logger.log_interaction() during this method!
        # print("running interaction")
        # assert random_person.is_alive == True
        # assert sick_person.is_alive == True
        did_infect = False
        is_random_person_vaccinated = True
        is_random_person_sick = False
        if not random_person.is_vaccinated:
            random_number = random.random()
            if self.basic_repro_num > random_number:
                self.newly_infected.append(random_person._id)
                did_infect = True
                is_random_person_sick = True
        # print("len of newly infected:", len(self.newly_infected))
        self.logger.log_interaction(sick_person, random_person, did_infect, random_person.is_vaccinated, is_random_person_sick)

    # TODO: Finish this method! This method should be called at the end of
    # every time step.  This method should iterate through the list stored in
    # self.newly_infected, which should be filled with the IDs of every person
    # created.  Iterate though this list.
    # For every person id in self.newly_infected:
    #   - Find the Person object in self.population that has this corresponding ID.
    #   - Set this Person's .infected attribute to True.
    # NOTE: Once you have iterated through the entire list of self.newly_infected, remember
    # to reset self.newly_infected back to an empty list!
    def _infect_newly_infected(self):
        count_sick_people = 0
        for person_id in self.newly_infected:
            for person in self.population:
                if person_id == person._id and person.infection == None and person.is_alive == True:
                    count_sick_people += 1
        self.current_infected += count_sick_people

        self.total_infected+= count_sick_people
        # print("sick ppl count", count_sick_people)
        print("CURR INF", self.current_infected)


        self.newly_infected.clear()

if __name__ == "__main__":
    params = sys.argv[1:]
    population_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(population_size, vacc_percentage, virus_name, mortality_rate,
                                basic_repro_num, initial_infected)
    simulation.run()
    simulation.logger.logger_file.close()
    # if debug:
    #     sim = Simulation(150, 0.4, "ryan", 0.6, 0.5)
    #     sim.run()
    #
    #     print(sim.current_infected)
    #     print(sim.dead_people)
    #     # print(len(sim.population))
    #     # print('debug mode')
    #
    # else:
    #     params = sys.argv[1:]
    #     print(params)
    #     pop_size = int(params[0])
    #     vacc_percentage = float(params[1])
    #     virus_name = str(params[2])
    #     mortality_rate = float(params[3])
    #     basic_repro_num = float(params[4])
    #     if len(params) == 6:
    #         initial_infected = int(params[5])
    #     else:
    #         initial_infected = 1
    #     simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
    #                             basic_repro_num, initial_infected)
    #     simulation.run()
