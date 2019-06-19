import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        isAuthenticated: false,

        errors: {
            'login': {
                'error': '',
                'email': "",
                'password': ""
            }
        },
        "currentView": Views.LOGIN,
        "showAddEditTaskModal": false,
        "showAddEditLabelModal": false,
        "addEditTaskModel": new AddEditTaskModel('add', {}),
        "addEditLabelModel": new AddEditLabelModel('add', {}),
        "goals": [],
        "goal": [],
        "LABELS": [],
        "TASKS": [],
        "TASKS_MAP": {}
    },
    mutations: {

        AUTH_FAILED(state, error) {
            if (error.hasOwnProperty('Email')) {
                state.errors.login.email = error.Email[0];
            }
            if (error.hasOwnProperty('Password')) {
                state.errors.login.password = error.Password[0];
            }
            if (error.hasOwnProperty('Error')) {
                state.errors.login.error = error.Error;
            }
            NProgress.done()
        },

        AUTH_SUCCESS(state, data) {
            localStorage.setItem('auth_token', data.token)
            state.isAuthenticated = true
            NProgress.done()
            router.push({
                "name": Views.DASHBOARD
            })
        },

        SET_AUTH_STATUS(state, status) {
            state.isAuthenticated = status
            if (!status) {
                localStorage.removeItem('auth_token')
            }
        },

        SET_CURRENT_VIEW(state, view) {
            console.log('current-view:', view)
            state.currentView = view
            router.push({
                "name": view
            })
        },

        SET_GOALS(state, goals) {
            state.goals = []
            for (var i = 0; i < goals.length; i++) {
                state.goals.push(new GoalViewModel(false, goals[i]))
            }
            NProgress.done()
        },

        SET_GOAL(state, goal) {
            state.goal = goal
            state.LABELS = goal.labels
            NProgress.done()
        },

        ADD_GOAL(state) {
            NProgress.done()
        },

        EDIT_GOAL(state) {
            NProgress.done()
        },

        TOGGLE_GOAL_SELECT(state, goalVm) {
            goalVm.isSelected = !goalVm.isSelected;
        },

        SET_TASKS(state, data) {
            state.TASKS = data.goal.tasks
            for (var i = 0; i < data.goal.tasks.length; i++) {
                state.TASKS_MAP[data.goal.tasks[i].id] = data.goal.tasks[i]
            }
            NProgress.done()
        },

        SET_CHILD_TASKS(state, data) {
            let task = state.TASKS_MAP[data.task.id]
            console.log(task)
            if(!task.childTasks){
                task.childTasks = []
            }
            for (var i = 0; i < data.task.childTasks.length; i++) {
                state.TASKS_MAP[data.task.childTasks[i].id] = data.task.childTasks[i]
                task.childTasks.push(data.task.childTasks[i])
            }
            NProgress.done()
        },

        ADD_TASK(state) {
            NProgress.done()
        },

        EDIT_TASK(state) {
            NProgress.done()
        },


        ACTIVATE_ADD_EDIT_TASK_MODAL(state, addEditTaskModel) {
            state.addEditTaskModel = addEditTaskModel
            JQuery('#addedittaskmodal').modal();
        },

        DEACTIVATE_ADD_EDIT_TASK_MODAL(state, addEditTaskModel) {
            state.showAddEditTaskModal = false
            // JQuery('#addedittaskmodal').modal('hide');
        },

        ACTIVATE_ADD_EDIT_LABEL_MODAL(state, addEditLabelModel) {
            state.addEditLabelModel = addEditLabelModel
            JQuery('#addeditlabelmodal').modal();
        },

        ADD_LABEL(state) {
            NProgress.done()
        },

        EDIT_LABEL(state) {
            NProgress.done()
        },
    },
    actions: {

        authenticate({
            commit
        }, authDetails) {
            NProgress.start()
            let authParms = {
                'email': authDetails.email,
                'password': authDetails.password
            }
            AuthAPI.authenticate(authParms)
                .then(function (response) {
                    console.log(response)
                    commit('AUTH_SUCCESS', response.data)
                })
                .catch((e) => {
                    console.log(e.response.data)
                    commit('AUTH_FAILED', e.response.data)
                })

        },

        getGoals({
            commit
        }) {
            NProgress.start()
            GoalAPI.getAll()
                .then(function (response) {
                    commit('SET_GOALS', response.data.goals)
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        getGoal({
            commit
        }, goalId) {
            NProgress.start()
            GoalAPI.get(goalId)
                .then(function (response) {
                    commit('SET_GOAL', response.data.goal)
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        addGoal({
            commit
        }, newGoal) {
            NProgress.start()
            GoalAPI.add(newGoal)
                .then(function (response) {
                    console.log(response)
                    commit('ADD_GOAL')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        editGoal({
            commit
        }, editGoal) {
            NProgress.start()
            GoalAPI.edit(editGoal)
                .then(function (response) {
                    console.log(response)
                    commit('EDIT_GOAL')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        deleteGoals({
            dispatch,
            commit,
            state
        }) {
            NProgress.start()

            var goalsToDelete = []
            for (var i = 0; i < state.goals.length; i++) {
                if (state.goals[i].isSelected) {
                    goalsToDelete.push({
                        "title": state.goals[i].goal.title,
                        "slug": state.goals[i].goal.slug
                    })
                }
            }
            console.log(goalsToDelete)

            GoalAPI.delete(goalsToDelete)
                .then(function (response) {
                    dispatch('getGoals');
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        getTasks({
            commit
        }, goalId) {
            NProgress.start()
            GoalAPI.get(goalId)
                .then(function (response) {
                    commit('SET_TASKS', response.data)
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        getChildTasks({
            commit
        }, taskId) {
            NProgress.start()
            TaskAPI.get(taskId)
                .then(function (response) {
                    commit('SET_CHILD_TASKS', response.data)
                })
                .catch((e) => {
                    console.log(e)
                    NProgress.done()
                })

        },

        addTask({
            commit
        }, newTask) {
            NProgress.start()
            TaskAPI.add(newTask)
                .then(function (response) {
                    commit('ADD_TASK')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        editTask({
            commit
        }, task) {
            NProgress.start()
            TaskAPI.edit(task)
                .then(function (response) {
                    commit('EDIT_TASK')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        addLabel({
            commit
        }, newLabel) {
            NProgress.start()
            LabelAPI.add(newLabel)
                .then(function (response) {
                    commit('ADD_LABEL')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

        editLabel({
            commit
        }, label) {
            NProgress.start()
            LabelAPI.edit(label)
                .then(function (response) {
                    commit('EDIT_LABEL')
                })
                .catch((e) => {
                    console.log(e.response.data)
                    NProgress.done()
                })

        },

    }
})
