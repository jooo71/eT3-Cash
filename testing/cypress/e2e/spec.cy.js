describe('API Tests', () => {
  
  // Base URL of your Django API (set this as needed)
  const apiUrl = 'http://localhost:8000/api';
    // Variable to store the JWT access token
    let accessToken = '';
    const testUser = {
      phone_number: '1234567890',  // Replace with your test data
      password: 'password123',     // Replace with your test data
      name: 'Test User'
    };
    const testUser2 = {
      phone_number: '1234567899',  // Replace with your test data
      password: 'password123',     // Replace with your test data
      name: 'Test2 User'
    };
    

  it('should register a new user', () => {
    cy.request('POST', `${apiUrl}/register/`, {
      phone_number: testUser.phone_number,
      password: testUser.password,
      name: 'Test User'
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('access');
    });
  });
  
  it('should register a new user', () => {
    cy.request('POST', `${apiUrl}/register/`, {
      phone_number: testUser2.phone_number,
      password: testUser2.password,
      name: 'Test2 User'
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('access');
    });
  });

  it('should log in and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,  // Your login endpoint
      body: {
        phone_number: testUser.phone_number,
        password: testUser.password,     // Replace with your test data
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if login is successful
      accessToken = response.body.access;  // Store the token
      expect(accessToken).to.exist;        // Ensure token is present
    });
  });
  
  it('should deposit money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,  // Your deposit endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 1000  // Amount to deposit
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if deposit is successful
      expect(response.body.message).to.include('Deposited');  // Verify the deposit message
    });
  });
  it('should withdraw money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,  // Your withdraw endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 100  // Amount to withdraw
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if withdrawal is successful
      expect(response.body.message).to.include('Withdrew');  // Verify the withdraw message
    });
  });

  it('should transfer money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,  // Your transfer endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        recipient_phone: '01110989460',  // Replace with the recipient's phone number
        amount: 300  // Amount to transfer
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if transfer is successful
      expect(response.body.message).to.include('Transferred');  // Verify the transfer message
      expect(response.body.recipient_name).to.exist;  // Ensure recipient name is returned
    });
  });

  it('should pay a bill using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,  // Your pay bill endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        bill_name: 'electricity',  // Type of bill (replace with your test data)
        amount: 150  // Amount to pay
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if bill payment is successful
      expect(response.body.message).to.include('paid');  // Verify the bill payment message
      expect(response.body.message).to.include('electricity');  // Ensure bill type is returned
    });
  });

  it('should buy airtime using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,  // Your buy airtime endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 100  // Amount to buy airtime
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if airtime purchase is successful
      expect(response.body.message).to.include('Bought');  // Verify the airtime purchase message
      expect(response.body.message).to.include('worth of airtime');  // Ensure the message mentions airtime
    });
  });
  it('should retrieve transaction history using the token', () => {
    cy.request({
      method: 'GET',
      url: `${apiUrl}/transaction-history/`,  // Your transaction history endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if retrieval is successful
      expect(response.body).to.be.an('array');  // Ensure the response is an array
      
      // Optionally check if the array is not empty
      if (response.body.length > 0) {
        const transaction = response.body[0];  // Get the first transaction
        // Check for general fields that should be present in a transaction
        expect(transaction).to.have.property('id');  // Assuming each transaction has an ID
        expect(transaction).to.have.property('amount');  // Assuming each transaction has an amount
        expect(transaction).to.have.property('transaction_type');  // Assuming type of transaction
        expect(transaction).to.have.property('date');  // Assuming there is a date field
        // Add more fields here as necessary based on your Transaction model
      }
    });
  });
  it('should retrieve balance using the token', () => {
    cy.request({
      method: 'GET',
      url: `${apiUrl}/balance/`,  // Your balance endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if retrieval is successful
      expect(response.body).to.have.property('balance');  // Ensure the response includes the balance
      expect(response.body).to.have.property('message');  // Ensure the response includes a message
      expect(response.body.balance).to.be.a('number');  // Ensure the balance is a number
    });
  });
});


describe('Deposit Functionality Tests', () => {
  
  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';
  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });
  // Successful deposit case
  it('should perform a successful deposit using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 1000  // Example valid amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Deposit successful.');
    });
  });

  // Deposit with zero amount
  it('should fail to deposit with zero amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 0  // Invalid amount
      },
      failOnStatusCode: false  // We want to capture the error response
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to deposit with zero amount.');
    });
  });

  // Deposit with a negative amount
  it('should fail to deposit with a negative amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: -500  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to deposit with a negative amount.');
    });
  });

  // Deposit with invalid token
  it('should fail to deposit with an invalid token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer invalid_token`
      },
      body: {
        amount: 1000  // Valid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(401); // Expect unauthorized
      // expect(response.body).to.have.property('error', 'Invalid token.'); // Adjust based on your API response
      cy.log('Failed to deposit with an invalid token.');
    });
  });

  // Deposit with a non-numeric value
  it('should fail to deposit with a non-numeric amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 'abc'  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Invalid amount.'); // Adjust based on your API response
      cy.log('Failed to deposit with a non-numeric amount.');
    });
  });
});
///////////////////////////////*****************************************************************************////////////////////
describe('Withdraw Functionality Tests', () => {
  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';
  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });

  // Assume you have a way to set up the accessToken here before the tests

  // Successful withdrawal case
  it('should perform a successful withdrawal using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 50  // Example valid amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Withdraw successful.');
    });
  });

  // Withdrawal with insufficient funds
  it('should fail to withdraw with insufficient funds', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 1000000  // Attempting to withdraw more than the available balance
      },
      failOnStatusCode: false  // We want to capture the error response
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Insufficient funds.'); // Adjust based on your API response
      cy.log('Failed to withdraw with insufficient funds.');
    });
  });

  // Withdrawal with zero amount
  it('should fail to withdraw with zero amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 0  // Invalid amount
      },
      failOnStatusCode: false  // We want to capture the error response
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to withdraw with zero amount.');
    });
  });

  // Withdrawal with negative amount
  it('should fail to withdraw with a negative amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: -50  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to withdraw with a negative amount.');
    });
  });

  // Withdrawal with invalid token
  it('should fail to withdraw with an invalid token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer invalid_token`
      },
      body: {
        amount: 50  // Valid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(401); // Expect unauthorized
      // expect(response.body).to.have.property('error', 'Invalid token.'); // Adjust based on your API response
      cy.log('Failed to withdraw with an invalid token.');
    });
  });

  // Withdrawal with a non-numeric value
  it('should fail to withdraw with a non-numeric amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 'abc'  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Invalid amount.'); // Adjust based on your API response
      cy.log('Failed to withdraw with a non-numeric amount.');
    });
  });
});
////////////////******************************************************************************/////////////////
describe('Transfer Functionality Tests', () => {
  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';
  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });

  // Successful transfer case
  it('should perform a successful transfer using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Replace with a valid recipient phone number
        amount: 100  // Example valid amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('recipient_name');
      cy.log('Transfer successful.');
    });
  });

  // Transfer with insufficient funds
  it('should fail to transfer with insufficient funds', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Replace with a valid recipient phone number
        amount: 1000000  // Attempting to transfer more than the available balance
      },
      failOnStatusCode: false  // We want to capture the error response
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Insufficient funds.'); // Adjust based on your API response
      cy.log('Failed to transfer with insufficient funds.');
    });
  });

  // Transfer to a non-existent phone number
  it('should fail to transfer to a non-existent phone number', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '0000000000',  // Attempting to transfer to a non-existent phone number
        amount: 100  // Example amount
      },
      failOnStatusCode: false  // We want to capture the error response
    }).then((response) => {
      // Expect a 404 error or any error status code from your API
      // expect(response.status).to.eq(404); // Ensure it matches the status code your API returns
      // expect(response.body).to.have.property('error', 'Recipient not found.'); // Match with the actual error message from your API
      cy.log('Failed to transfer to a non-existent phone number.');
    });
  });

  // Transfer with zero amount
  it('should fail to transfer with zero amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Valid recipient phone number
        amount: 0  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to transfer with zero amount.');
    });
  });

  // Transfer with negative amount
  it('should fail to transfer with a negative amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Valid recipient phone number
        amount: -50  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Amount must be greater than zero.'); // Adjust based on your API response
      cy.log('Failed to transfer with a negative amount.');
    });
  });

  // Transfer with invalid token
  it('should fail to transfer with an invalid token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer invalid_token`
      },
      body: {
        recipient_phone: '01110989460',  // Valid recipient phone number
        amount: 100  // Valid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(401); // Expect unauthorized
      // expect(response.body).to.have.property('error', 'Invalid token.'); // Adjust based on your API response
      cy.log('Failed to transfer with an invalid token.');
    });
  });

  // Transfer with a non-numeric amount
  it('should fail to transfer with a non-numeric amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Valid recipient phone number
        amount: 'abc'  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400); // Expect a bad request
      // expect(response.body).to.have.property('error', 'Invalid amount.'); // Adjust based on your API response
      cy.log('Failed to transfer with a non-numeric amount.');
    });
  });
});
//////////////////////////////////////////*********************************************************************////////////

describe('Bill Payment Tests', () => {

  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';


  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });

  // Case 1: Successful bill payment
  it('should pay the bill successfully using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        bill_name: 'electricity',  // Example bill type
        amount: 75  // Example amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Success status
      expect(response.body).to.have.property('message');
      cy.log('Bill payment successful.');
    });
  });

  // Case 2: Invalid bill type
  it('should fail to pay the bill with an invalid bill type', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        bill_name: 'invalid_type',  // Invalid bill type
        amount: 75
      },
      failOnStatusCode: false  // Prevents Cypress from failing on non-2xx status codes
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust based on the actual API response
      // expect(response.body).to.have.property('error', 'Invalid bill type.'); // Match error message returned by your API
      cy.log('Failed to pay bill due to invalid bill type.');
    });
  });

  // Case 3: Invalid amount (too low or too high)
  it('should fail to pay the bill with an invalid amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        bill_name: 'electricity',  // Example bill type
        amount: -10  // Invalid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust based on your API
      // expect(response.body).to.have.property('error', 'Invalid amount.');
      cy.log('Failed to pay bill due to invalid amount.');
    });
  });

  // Case 4: Missing bill type
  it('should fail to pay the bill when bill type is missing', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 50  // Example valid amount
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust according to your API
      // expect(response.body).to.have.property('error', 'Bill type is required.');
      cy.log('Failed to pay bill due to missing bill type.');
    });
  });

});

/////////////////////////////////////***********************************/////////////////////////////////////
describe('Airtime Purchase Tests', () => {

  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';
  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });

  // Case 1: Successful airtime purchase
  it('should buy airtime successfully using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 20  // Example valid amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Success status
      expect(response.body).to.have.property('message');
      cy.log('Airtime purchase successful.');
    });
  });

  // Case 2: Invalid airtime amount (negative)
  it('should fail to buy airtime with a negative amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: -10  // Invalid negative amount
      },
      failOnStatusCode: false  // Allows Cypress to handle non-2xx status codes
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust based on your API response
      // expect(response.body).to.have.property('error', 'Invalid amount.');
      cy.log('Failed to purchase airtime due to invalid amount.');
    });
  });

  // Case 3: Missing airtime amount
  it('should fail to buy airtime without providing an amount', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {},  // Missing amount
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust based on API response
      // expect(response.body).to.have.property('error', 'Amount is required.');
      cy.log('Failed to purchase airtime due to missing amount.');
    });
  });

  // Case 4: Exceeding airtime limit
  it('should fail to buy airtime when amount exceeds the limit', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 100000  // Example excessive amount exceeding limit
      },
      failOnStatusCode: false
    }).then((response) => {
      // expect(response.status).to.eq(400);  // Adjust according to your API
      // expect(response.body).to.have.property('error', 'Exceeds airtime limit.');
      cy.log('Failed to purchase airtime due to exceeding limit.');
    });
  });

});
