import http from 'k6/http'
import { sleep } from 'k6'

/**
 * Scenario:
 * 200 users sending requests every 1s
 *
 * Usage:
 * k6 run getTodos.test.js
 */

export const options = {
  stages: [
    { duration: '10s', target: 200 }, // ramp-up
    { duration: '10s', target: 200 }, // stable
    { duration: '10s', target: 0 } // ramp-down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
    http_req_duration: ['p(99)<200'] // 99% of requests should be below 200ms
  }
}

export default function () {
  http.get('https://corndel-todo-pr-1.onrender.com/todos')
  sleep(1)
}
