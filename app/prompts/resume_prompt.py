def generate_prompt(github_data):
    return f'''
    Based on the following GitHub data, generate a resume:
    {github_data}
    '''
    