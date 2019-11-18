from app import app
from app.forms import LoginForm
from flask import request, render_template, flash, redirect, url_for
import pandas as pd
import calendar


@app.route('/', methods=['GET','POST'])
def index():
    import calendar
    from pprint import pprint
    pprint(request.form)
    form = LoginForm()
    if 'feature_one' in request.form and 'feature_two' in request.form and 'month' in request.form and 'team' in request.form:
        team = request.form['team']
        feature_one = request.form['feature_one']
        feature_two = request.form['feature_two']
        month = (request.form['month'])
        df = pd.read_pickle('data/final_preds/final_pred.pkl')
        df = df[df['TEAM_HOME'] == team]
        df = df[df['DATE_HOME'].apply(lambda x: x.month) == int(month)]
        df['TEAM_HOME'] = df['TEAM_HOME'].apply(lambda x: x.title().replace('_',' '))
        df['TEAM_AWAY'] = df['TEAM_AWAY'].apply(lambda x: x.title().replace('_',' '))
        if len(df) == 1:

            df.reset_index(inplace=True)

            # sort the values by the feature one
            df.sort_values(by=[feature_one],ascending=False,inplace=True)

            # take the top game for suggested df
            suggested_df = df.copy()
            suggested_choice = suggested_df.iloc[0]
            suggested_choice_dict = suggested_choice.to_dict()

            month = calendar.month_name[int(month)]
            return render_template('one_feature_output.html',title='NBA Game Finder',
                                    suggested_choice=suggested_choice_dict,team=team,
                                    feature_one=feature_one,month=month,form=form)

        if len(df) == 2:

            df.reset_index(inplace=True)

            # sort the values by the feature one
            df.sort_values(by=[feature_one],ascending=False,inplace=True)

            # take the top 2 games for suggested df
            suggested_df = df.copy()
            suggested_choice = suggested_df.iloc[0]
            suggested_choice_dict = suggested_choice.to_dict()
            feature_one_choice = suggested_df.iloc[1]
            feature_one_choice_dict = feature_one_choice.to_dict()

            month = calendar.month_name[int(month)]
            return render_template('one_feature_output.html',title='NBA Game Finder',feature_one_choice=feature_one_choice_dict,
                                suggested_choice=suggested_choice_dict,team=team,feature_one=feature_one,month=month,form=form)

        df.reset_index(inplace=True)

        # sort the values by the feature one
        df.sort_values(by=[feature_one],ascending=False,inplace=True)

        # take the top 3 games for suggested df
        suggested_df = df.iloc[:3].copy()
        suggested_df.sort_values(by=[feature_two],ascending=False,inplace=True)
        suggested_choice = suggested_df.iloc[0]
        suggested_choice_dict = suggested_choice.to_dict()
        # drop the suggested_choice from the original index
        df.drop(index=suggested_choice.name, inplace=True)

        ## get the other recommended games
        # feature_one
        df.sort_values(by=[feature_one],ascending=False, inplace=True)
        feature_one_choice = df.iloc[0].copy()
        feature_one_choice_dict = feature_one_choice.to_dict()
        # drop the feature_one_choice from the original index
        df.drop(index=feature_one_choice.name, inplace=True)

        # feature_two
        df.sort_values(by=[feature_two],ascending=False, inplace=True)
        feature_two_choice = df.iloc[0].copy()
        feature_two_choice_dict = feature_two_choice.to_dict()
        month = calendar.month_name[int(month)]
        
        return render_template('three_feature_output.html',title='NBA Game Finder',feature_one_choice=feature_one_choice_dict,feature_two_choice=feature_two_choice_dict,
                                suggested_choice=suggested_choice_dict,team=team,feature_one=feature_one,feature_two=feature_two,month=month,form=form)
    
    return render_template('homepage.html', title='NBA Game Finder', form=form)

