var weatherModule = (function() {
	"use strict";
	var owm = {
		init: function() {
			this.cacheDom();
			this.bindEvents();
			this.callAPI();
		},
		cacheDom: function() {
			this.xBx = $("#xBxHack");
			this.user_input = $("#userCity");
			this.forcast = $("#forcast");
			this.city = $("#city");
			this.temp = $("#temperature");
			this.tempHigh = $("#high");
			this.tempLow = $("#low");
			this.set_icon = $("#set-icon").parent();
			this.weat_icon = $("#weather-icon");
			this.weat_icon_class = function(time_of_day) {
				var iconClass = "wi-owm-";

				if (time_of_day === "PM") {
					iconClass += "night-";
				} else {
					iconClass += "day-";
				}
				return iconClass;
			};
		},
		bindEvents: function() {
			this.city.click(this.events.checkBox.bind(this));
			this.city.hover(this.events.hover.bind(this));
			this.set_icon.click(this.events.checkBox.bind(this));
			this.user_input.keypress(this.events.enterKey.bind(this));
			this.user_input.blur(this.events.resetCheckBox.bind(this));
		},
		events: {
			checkBox: function(e) {
				e.preventDefault();
				this.xBx.prop("checked", true);
				this.user_input.focus();
			},
			resetCheckBox: function(e) {
				e.preventDefault();
				if (e.type === "keypress") {
					this.user_input.blur();
				}
				this.user_input.val("");
				this.xBx.prop("checked", false);
			},
			hover: function(e) {
				this.set_icon.toggleClass("hovered");
			},
			enterKey: function(e) {
				if (e.which === 13 || e.keyCode === 13) {
					e.preventDefault();
					this.callAPI(this.user_input.val());
					this.events.resetCheckBox.apply(this, [e]);
				}
			}
		},
		callAPI: function(url) {
			var apiUrl =
				"//api.openweathermap.org/data/2.5/weather?APPID=d65a9694ae6425d1e080326aab19db69&units=imperial&q=";
			if (url === undefined || url === "") {
				url =
					"//api.openweathermap.org/data/2.5/weather?APPID=d65a9694ae6425d1e080326aab19db69&units=imperial&q=san%20diego";
			} else {
				while (url.charAt(0) === " ") {
					url = url.substr(1);
				}
				apiUrl += encodeURIComponent(url);
				url = apiUrl.toLowerCase();
			}
			$.getJSON(url, this.parseData.bind(this));
		},
		parseData: function(json) {
			this.data = {
				name: json.name,
				weather: {
					description: json.weather[0].description,
					id: json.weather[0].id
				},
				temp: {
					current: Math.floor(json.main.temp),
					high: Math.floor(json.main.temp_max),
					low: Math.floor(json.main.temp_min)
				}
			};
			this.renderHTML();
		},
		renderHTML: function() {
			this.city.html(this.data.name);
			this.forcast.html(this.data.weather.description);
			this.temp.html(this.data.temp.current);
			this.tempHigh.html(this.data.temp.high);
			this.tempLow.html(this.data.temp.low);
			//DELETE CLASSES
			this.weat_icon.removeClass();
			//RESET CLASSES
			this.weat_icon.addClass("wi wi-fw weather-icon ");
			//ADD NEW CLASS
			this.weat_icon.addClass(this.weat_icon_class() + this.data.weather.id);
		}
	};
	owm.init();
	return {
		time_of_day: owm.weat_icon_class
	};
})();
var timeModule = (function() {
	"use strict";
	var dateTime = {
		init: function() {
			this.cacheDom();
			this.render();
			this.refresh();
		},
		cacheDom: function() {
			this.date = new Date();
			this.time = $("#time");
			this.day = $("#day");
			this.month = $("#monDate");
		},
		refresh: function() {
			setInterval(function() {
				dateTime.date = new Date();
				dateTime.render();
			}, 1000);
		},
		render: function() {
			var currentMonth = [
					"Jan",
					"Feb",
					"Mar",
					"Apr",
					"May",
					"Jun",
					"Jul",
					"Aug",
					"Sep",
					"Oct",
					"Nov",
					"Dec"
				],
				currentDay = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
				month = this.date.getMonth(),
				date = this.date.getDate(),
				hour = this.date.getHours(),
				minutes = this.date.getMinutes(),
				day = this.date.getDay(),
				amPM;

			/* CHECK TIME
						--------------------------------*/
			//IF MIDNIGHT
			if (hour === 0) {
				//HOUR EQUALS 12
				hour = 12;
			}
			//CHANGE 24 HOUR TO 12 HOUR
			if (hour > 12) {
				//MINUS 12
				hour -= 12;
				//CHANGE TO PM
				amPM = "PM";
			} else {
				//CHANGE TO AM
				amPM = "AM";
			}
			//IF HOUR IS LESS THAN 10
			if (hour < 10) {
				//ADD 0 TO HOUR
				hour = "0" + hour;
			}
			//GET MINUTES
			//IF MINUTES LESS THAN 10
			if (minutes < 10) {
				//ADD 0 TO MINUTES
				minutes = "0" + minutes;
			}
			//RENDER TIME
			this.time.html(hour + ":" + minutes + "<span>" + amPM + "</span>");
			//SET TIME OF DAT
			weatherModule.time_of_day(amPM);
			//RENDER DAY
			this.day.html(currentDay[day]);
			//RENDER DATE
			this.month.html(currentMonth[month] + " " + date);
		}
	};
	dateTime.init();
})();
